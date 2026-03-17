from typing import Protocol, List, Any, Dict, runtime_checkable
import multiprocessing


@runtime_checkable
class DataSink(Protocol):
    
    def write(self, results: dict) -> None: ...

@runtime_checkable
class PipelineService(Protocol):
  
    def run(self) -> None: ...


@runtime_checkable
class TelemetryObserver(Protocol):
   
    def on_telemetry_update(self, metrics: Dict[str, Any]) -> None: ...


@runtime_checkable
class TelemetrySubject(Protocol):
   
    def subscribe(self, observer: TelemetryObserver) -> None: ...
    def unsubscribe(self, observer: TelemetryObserver) -> None: ...
    def notify_observers(self, metrics: Dict[str, Any]) -> None: ...

class DataPacket:
    """
    A domain-agnostic unit of data travelling through the pipeline.
    Fields are driven entirely by schema_mapping in config.json.
    """
    __slots__ = ("entity_name", "time_period", "metric_value",
                 "security_hash", "extra_fields", "is_verified",
                 "computed_metric", "worker_id")

    def __init__(
        self,
        entity_name: str       = "",
        time_period: int       = 0,
        metric_value: float    = 0.0,
        security_hash: str     = "",
        extra_fields: dict     = None,
        is_verified: bool      = False,
        computed_metric: float = 0.0,
        worker_id: int         = -1,
    ):
        self.entity_name     = entity_name
        self.time_period     = time_period
        self.metric_value    = metric_value
        self.security_hash   = security_hash
        self.extra_fields    = extra_fields or {}
        self.is_verified     = is_verified
        self.computed_metric = computed_metric
        self.worker_id       = worker_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_name":     self.entity_name,
            "time_period":     self.time_period,
            "metric_value":    self.metric_value,
            "security_hash":   self.security_hash,
            "extra_fields":    self.extra_fields,
            "is_verified":     self.is_verified,
            "computed_metric": self.computed_metric,
            "worker_id":       self.worker_id,
        }

    def __repr__(self) -> str:
        return (f"DataPacket(entity={self.entity_name!r}, "
                f"t={self.time_period}, val={self.metric_value:.4f}, "
                f"verified={self.is_verified})")

SENTINEL = None 