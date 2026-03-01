import csv
import json
import os
from typing import List, Dict, Any


class CSVReader:
    """CSV file reader implementation"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read(self) -> List[Dict[str, Any]]:
        """Read data from CSV file"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                data = list(reader)
            
            if not data:
                raise ValueError("CSV file is empty")
            
            print(f" Loaded {len(data)} records from CSV")
            return data
        
        except Exception as e:
            raise Exception(f"Error reading CSV: {str(e)}")
    
    def validate(self, data: List[Dict[str, Any]]) -> bool:
        """Validate CSV data structure"""
        if not data:
            raise ValueError("No data to validate")
        
        required_columns = ['Country Name', 'Continent']
        first_row = data[0]
        
        missing = [col for col in required_columns if col not in first_row.keys()]
        
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        
        return True
    
    class JSONReader:
     """JSON file reader implementation"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read(self) -> List[Dict[str, Any]]:
        """Read data from JSON file"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"JSON file not found: {self.file_path}")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Handle both list and dict formats
            if isinstance(data, dict):
                if 'data' in data:
                    data = data['data']
                elif 'records' in data:
                    data = data['records']
                else:
                    data = [data]
            
            if not data:
                raise ValueError("JSON file is empty")
            
            print(f"✓ Loaded {len(data)} records from JSON")
            return data
        
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise Exception(f"Error reading JSON: {str(e)}")
    
    def validate(self, data: List[Dict[str, Any]]) -> bool:
        """Validate JSON data structure"""
        if not data:
            raise ValueError("No data to validate")
        
        required_fields = ['Country Name', 'Continent']
        first_record = data[0]
        
        missing = [field for field in required_fields if field not in first_record]
        
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        
        return True