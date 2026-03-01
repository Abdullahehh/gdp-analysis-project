
from typing import List, Any
from core.contracts import DataSink
from functools import reduce


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

    @staticmethod
    def load_gdp_data(file_path: str) -> List[dict]:
    #phase 1 se data load kre ga
        return load_gdp_data(file_path)

    #required sari outputs is me print hon gi
    def _run_all_analyses(self, all_data: List[dict], filtered_data: List[dict]) -> dict:
        """Runs all 8 required outputs and returns a single results dictionary."""
        config        = self.config
        region        = config["region"]
        year          = int(config["year"])
        date_range    = config.get("date_range", [2000, 2020])
        decline_years = config.get("decline_years", 5)
        operation     = config.get("operation", "sum")

        print("\n Running all 8 analyses...")

        results = {
            "top_10":                 self._top_n_countries(filtered_data, n=10, ascending=False),
            "bottom_10":              self._top_n_countries(filtered_data, n=10, ascending=True),
            "growth_rate":            self._gdp_growth_rate(all_data, region, date_range),
            "avg_by_continent":       self._avg_gdp_by_continent(all_data, date_range),
            "global_gdp_trend":       self._global_gdp_trend(all_data, date_range),
            "fastest_growing":        self._fastest_growing_continent(all_data, date_range),
            "consistent_decline":     self._consistent_decline(all_data, decline_years),
            "continent_contribution": self._continent_contribution(all_data, date_range),
            "meta": {
                "region":        region,
                "year":          year,
                "date_range":    date_range,
                "decline_years": decline_years,
                "operation":     operation,
            }
        }

        print(" All 8 analyses complete.")
        return results
    
    #output 1 and 2
    def _top_n_countries(self, filtered_data: List[dict], n: int, ascending: bool) -> List[dict]:
        if not filtered_data:
            return []
        
        sorted_data = sorted(filtered_data, key=lambda x: x["value"], reverse=not ascending)
      
        return list(map(
            lambda r: {"country": r["country"], "gdp": r["value"]},
            sorted_data[:n]
        ))
    
     #output 3

    def _gdp_growth_rate(self, all_data: List[dict], region: str, date_range: list) -> dict:
        start, end   = date_range
        region_lower = region.strip().lower()

        regions = (
            list(map(str.strip, region_lower.split('&'))) if '&' in region_lower else
            list(map(str.strip, region_lower.split(','))) if ',' in region_lower else
            [region_lower]
        )

        region_data = list(filter(
            lambda r: r["continent"].strip().lower() in regions
                      and r["year"] in [start, end],
            all_data
        ))

        by_country = reduce(
            lambda acc, r: {
                **acc,
                r["country"]: {**acc.get(r["country"], {}), r["year"]: r["value"]}
            },
            region_data,
            {}
        )

        valid = filter(
            lambda item: start in item[1] and end in item[1] and item[1][start] > 0,
            by_country.items()
        )

        return dict(map(
            lambda item: (
                item[0],
                round(((item[1][end] - item[1][start]) / item[1][start]) * 100, 2)
            ),
            valid
        ))
    
     # output 4
    def _avg_gdp_by_continent(self, all_data: List[dict], date_range: list) -> dict:
        start, end = date_range

       
        in_range = list(filter(lambda r: start <= r["year"] <= end, all_data))

        if not in_range:
            return {}

        by_continent = reduce(
            lambda acc, r: {
                **acc,
                r["continent"]: acc.get(r["continent"], []) + [r["value"]]
            },
            in_range,
            {}
        )

        return dict(map(
            lambda item: (item[0], round(sum(item[1]) / len(item[1]), 2)),
            by_continent.items()
        ))
    
    #output 5
    
    def _global_gdp_trend(self, all_data: List[dict], date_range: list) -> dict:
        start, end = date_range

       
        in_range = list(filter(lambda r: start <= r["year"] <= end, all_data))

        if not in_range:
            return {}

       
        by_year = reduce(
            lambda acc, r: {**acc, r["year"]: acc.get(r["year"], 0) + r["value"]},
            in_range,
            {}
        )

       
        return dict(sorted(by_year.items(), key=lambda x: x[0]))