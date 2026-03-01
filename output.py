import json
import csv
import os
from typing import List, Dict, Any

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.visualizer import pie_chart, bar_chart, line_chart, scatter_chart


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

class GraphicsChartWriter:
    
    def __init__(self, output_dir: str = 'visualizations'):
       
        self.output_dir = output_dir
        
        # Create directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def write(self, records: List[Dict[str, Any]]) -> None:
        
        if not records:
            print("  No data to visualize")
            return
        
        try:
            
            data_dict = self._prepare_data(records)
            
            if not data_dict:
                print(" Could not prepare data for visualization")
                return
            
  
            self._create_all_charts(data_dict, records)
            
            print(f" Charts saved in {self.output_dir}/")
        
        except ImportError:
            print(" Could not import Phase 1 visualizer. Make sure modules/visualizer.py exists")
        except Exception as e:
            print(f" Error creating charts: {str(e)}")
    
    def _prepare_data(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
       
        if not records:
            return {}
        
        first_record = records[0]
        
        # If we have 'Country' and 'GDP' then country ranking data
        if 'Country' in first_record and 'GDP' in first_record:
            return {record['Country']: record['GDP'] for record in records}
        
        # If we have 'Year' then time series data
        if 'Year' in first_record:
            value_field = [k for k in first_record.keys() if k != 'Year'][0]
            return {record['Year']: record[value_field] for record in records}
        
        #If we have 'Continent' then continental data
        if 'Continent' in first_record:
            value_field = [k for k in first_record.keys() if k != 'Continent'][0]
            return {record['Continent']: record[value_field] for record in records}
        
        # Generic then use first two fields
        keys = list(first_record.keys())
        if len(keys) >= 2:
            return {record[keys[0]]: record[keys[1]] for record in records}
        
        return {}
    
    def _create_all_charts(self, data_dict: Dict[str, Any], records: List[Dict[str, Any]]) -> None:
       
        first_record = records[0]
        
        # Determine labels
        if 'Country' in first_record:
            xlabel = 'Country'
            ylabel = 'GDP (USD)'
            title_suffix = 'by Country'
        elif 'Year' in first_record:
            xlabel = 'Year'
            ylabel = 'Value'
            title_suffix = 'Over Time'
        elif 'Continent' in first_record:
            xlabel = 'Continent'
            ylabel = 'GDP (USD)'
            title_suffix = 'by Continent'
        else:
            xlabel = 'Category'
            ylabel = 'Value'
            title_suffix = 'Comparison'
        
        bar_path = os.path.join(self.output_dir, 'output_bar_chart.png')
        bar_chart(
            data_dict,
            f'Bar Chart - {title_suffix}',
            xlabel,
            ylabel,
            bar_path
        )
        
        # pie chart if we have categorical data 
        if 'Year' not in first_record:
            pie_path = os.path.join(self.output_dir, 'output_pie_chart.png')
            pie_chart(
                data_dict,
                f'Distribution - {title_suffix}',
                pie_path
            )
        
        # line chart for trend data
        if 'Year' in first_record or len(data_dict) > 3:
            line_path = os.path.join(self.output_dir, 'output_line_chart.png')
            line_chart(
                data_dict,
                f'Trend - {title_suffix}',
                xlabel,
                ylabel,
                line_path
            )
        
        # scatter chart for numerical relationships
        if len(data_dict) > 5:
            scatter_path = os.path.join(self.output_dir, 'output_scatter_chart.png')
            scatter_chart(
                data_dict,
                f'Scatter Plot - {title_suffix}',
                xlabel,
                ylabel,
                scatter_path
            )




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