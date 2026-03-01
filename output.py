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
            
            print(f" Data saved to {self.output_path}")
        
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


class HTMLReportWriter:
    """generates formatted HTML reports"""
    
    def __init__(self, output_path: str = 'report.html'):
        self.output_path = output_path
    
    def write(self, records: List[Dict[str, Any]]) -> None:
       
        if not records:
            print(" No data to write")
            return
        
        try:
            html = self._generate_html(records)
            
            with open(self.output_path, 'w', encoding='utf-8') as file:
                file.write(html)
            
            print(f" HTML report saved to {self.output_path}")
        
        except Exception as e:
            print(f" Error creating HTML report: {str(e)}")
    
    def _generate_html(self, records: List[Dict[str, Any]]) -> str:
        
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GDP Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        h1 { color: #333; text-align: center; }
        table { width: 100%; border-collapse: collapse; background-color: white; }
        th { background-color: #4CAF50; color: white; padding: 12px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:hover { background-color: #f1f1f1; }
    </style>
</head>
<body>
    <h1>GDP Analysis Report</h1>
    <p>Total Records: """ + str(len(records)) + """</p>
    <table>
        <thead><tr>"""
        
        if records:
            for key in records[0].keys():
                html += f"<th>{key}</th>"
        
        html += "</tr></thead><tbody>"
        
        for record in records:
            html += "<tr>"
            for value in record.values():
                if isinstance(value, float):
                    html += f"<td>${value:,.2f}</td>"
                else:
                    html += f"<td>{value}</td>"
            html += "</tr>"
        
        html += "</tbody></table></body></html>"
        
        return html