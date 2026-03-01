from typing import Protocol, List, Any, runtime_checkable


@runtime_checkable
class DataSink(Protocol):
   # jo bhi class write(results: dict) method rakhegi, use DataSink maana jayega.
    def write(self, results: dict) -> None:
        ...

        
@runtime_checkable
class PipelineService(Protocol):
  #koi bhi class jo execute(raw_data: List[Any]) method rakhe, use PipelineService maana jayega.
    def execute(self, raw_data: List[Any]) -> None:
        ...
