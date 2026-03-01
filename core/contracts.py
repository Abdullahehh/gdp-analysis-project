from typing import Protocol, List, Any, runtime_checkable


@runtime_checkable
class DataSink(Protocol):
   # jo bhi class write(results: dict) method rakhegi, use DataSink maana jayega.
    def write(self, results: dict) -> None:
        ...