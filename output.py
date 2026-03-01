import json
import csv
from typing import List, Dict, Any


class ConsoleWriter:
    """ displays results in terminal"""
    
    def write(self, records: List[Dict[str, Any]]) -> None:
        """Write records to console"""
        if not records:
            print(" No data to display")
            return
        
        print("\n" + "="*80)
        print("  RESULTS")
        print("="*80)
        
        for i, record in enumerate(records, 1):
            print(f"\n{i}. ", end="")
            
            for key, value in record.items():
                if isinstance(value, float):
                    print(f"{key}: ${value:,.2f}", end="  |  ")
                else:
                    print(f"{key}: {value}", end="  |  ")
            
            print()
        
        print("\n" + "="*80)
        print(f"  Total Records: {len(records)}")
        print("="*80 + "\n")


class FileWriter:
    """saves results to CSV or JSON files"""
    
    def __init__(self, output_path: str, format: str = 'csv'):
        self.output_path = output_path
        self.format = format.lower()
        
        if self.format not in ['csv', 'json']:
            raise ValueError("Format must be 'csv' or 'json'")
    
    def write(self, records: List[Dict[str, Any]]) -> None:
        
        if not records:
            print(" No data to write")
            return
        
        try:
            if self.format == 'csv':
                self._write_csv(records)
            else:
                self._write_json(records)
            
            print(f"✓ Data saved to {self.output_path}")
        
        except Exception as e:
            print(f" Error writing file: {str(e)}")
    
    def _write_csv(self, records: List[Dict[str, Any]]) -> None:
        
        with open(self.output_path, 'w', newline='', encoding='utf-8') as file:
            if records:
                writer = csv.DictWriter(file, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
    
    def _write_json(self, records: List[Dict[str, Any]]) -> None:
        
        with open(self.output_path, 'w', encoding='utf-8') as file:
            json.dump(records, file, indent=2, ensure_ascii=False)


