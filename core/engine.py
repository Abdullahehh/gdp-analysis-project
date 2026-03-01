
from typing import List, Any
from core.contracts import DataSink


from modules.data_loader    import load_gdp_data, transform_data, clean_long_data
from modules.data_processor import filter_data, compute_stat

class TransformationEngine:
 

    def __init__(self, sink: DataSink, config: dict):
        
        if not isinstance(sink, DataSink):
            raise TypeError(
                f"'sink' must satisfy the DataSink protocol. "
                f"Got: {type(sink).__name__}"
            )
        self.sink   = sink
        self.config = config

        
    def execute(self, raw_data: List[Any]) -> None:
    
        if not raw_data:
            raise ValueError("execute() received empty data — nothing to process.")

        print("\n Engine received data. Starting processing...")

        long_data = transform_data(raw_data)
        print(f" Transformed: {len(long_data)} records")

        if not long_data:
            raise ValueError("Transformation produced zero records. Check your data file format.")

    
        cleaned = clean_long_data(long_data)
        print(f" Cleaned: {len(cleaned)} records")

        if not cleaned:
            raise ValueError("All records were removed during cleaning. Check data quality.")

      
        filtered = filter_data(cleaned, self.config)
        print(f" Filtered: {len(filtered)} records")

        if not filtered:
            region = self.config.get("region", "N/A")
            year   = self.config.get("year", "N/A")
            raise ValueError(
                f"No records found for region='{region}', year={year}. "
                f"Check region name and year in config.json."
            )

        results = self._run_all_analyses(cleaned, filtered)

        print("\n Sending results to output...")
        self.sink.write(results)
