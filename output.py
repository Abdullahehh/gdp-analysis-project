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


