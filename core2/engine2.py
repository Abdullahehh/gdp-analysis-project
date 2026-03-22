
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
