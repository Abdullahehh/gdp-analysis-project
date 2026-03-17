from typing import Protocol, List, Any, Dict, runtime_checkable
import multiprocessing


@runtime_checkable
class DataSink(Protocol):
    
    def write(self, results: dict) -> None: ...

@runtime_checkable
class PipelineService(Protocol):
  
    def execute(self, raw_data: List[Any]) -> None: ...


@runtime_checkable
class TelemetryObserver(Protocol):
   
    def on_telemetry_update(self, metrics: Dict[str, Any]) -> None: ...

