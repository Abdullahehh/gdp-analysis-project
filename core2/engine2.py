
def verify_signature(
    metric_value: float,
    entity_name: str,
    time_period: int,
    claimed_hash: str,
    secret_key: str,
    algorithm: str  = "pbkdf2_hmac",
    iterations: int = 100_000,
) -> bool:
   
    if not claimed_hash:
        return False

    try: # Build a deterministic message from the packet fields
        message = f"{entity_name}:{time_period}:{metric_value:.6f}".encode("utf-8")
        salt    = secret_key.encode("utf-8")

        if algorithm == "pbkdf2_hmac":
            digest = hashlib.pbkdf2_hmac(
                "sha256", message, salt, iterations
            ).hex()
        else:
          
            digest = hashlib.sha256(message + salt).hexdigest()

        return digest == claimed_hash

    except Exception:
        return False

def verify_signature(
    metric_value: float,
    entity_name: str,
    time_period: int,
    claimed_hash: str,
    secret_key: str,
    algorithm: str  = "pbkdf2_hmac",
    iterations: int = 100_000,
) -> bool:
    """
    Pure function.  Recompute the cryptographic hash from the raw fields and
    compare it with the attached signature.

    Uses PBKDF2-HMAC-SHA256 with the configured number of iterations.
    Returns True only when the digest matches exactly.
    """
    if not claimed_hash:
        return False

    try:
        # Build a deterministic message from the packet fields
        message = f"{entity_name}:{time_period}:{metric_value:.6f}".encode("utf-8")
        salt    = secret_key.encode("utf-8")

        if algorithm == "pbkdf2_hmac":
            digest = hashlib.pbkdf2_hmac(
                "sha256", message, salt, iterations
            ).hex()
        else:
            # Fallback: plain SHA-256 (useful for testing without heavy hashing)
            digest = hashlib.sha256(message + salt).hexdigest()

        return digest == claimed_hash

    except Exception:
        return False


def generate_signature(
    metric_value: float,
    entity_name: str,
    time_period: int,
    secret_key: str,
    algorithm: str  = "pbkdf2_hmac",
    iterations: int = 100_000,
) -> str:
   
    message = f"{entity_name}:{time_period}:{metric_value:.6f}".encode("utf-8")
    salt    = secret_key.encode("utf-8")

    if algorithm == "pbkdf2_hmac":
        return hashlib.pbkdf2_hmac("sha256", message, salt, iterations).hex()
    return hashlib.sha256(message + salt).hexdigest()


def compute_running_average(window: deque, new_value: float) -> float:
   
    if not window and new_value == 0.0:
        return 0.0
    total = sum(window) + new_value
    count = len(window) + 1
    return round(total / count, 6)



class CoreWorker:
    
    def __init__(
        self,
        worker_id:      int,
        raw_queue:      multiprocessing.Queue,
        verified_queue: multiprocessing.Queue,
        processing_cfg: Dict[str, Any],
        stats_queue:    multiprocessing.Queue,
    ):
        self.worker_id      = worker_id
        self.raw_queue      = raw_queue
        self.verified_queue = verified_queue
        self.processing_cfg = processing_cfg
        self.stats_queue    = stats_queue

        st = processing_cfg.get("stateless_tasks", {})
        self.secret_key  = st.get("secret_key",  "default_key")
        self.algorithm   = st.get("algorithm",   "pbkdf2_hmac")
        self.iterations  = int(st.get("iterations", 100_000))