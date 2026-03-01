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


class GraphicsChartWriter:
    """Graphics/Chart output writer - generates visual charts"""
    
    def __init__(self, output_dir: str = 'visualizations'):
        self.output_dir = output_dir
        
        import os
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def write(self, records: List[Dict[str, Any]]) -> None:
        """Generate charts from records"""
        if not records:
            print("⚠️  No data to visualize")
            return
        
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
            
            # Determine chart type based on data
            if self._is_ranking_data(records):
                self._create_bar_chart(records)
            elif self._is_trend_data(records):
                self._create_line_chart(records)
            elif self._is_distribution_data(records):
                self._create_pie_chart(records)
            else:
                self._create_bar_chart(records)
            
            print(f"✓ Charts saved in {self.output_dir}/")
        
        except ImportError:
            print("❌ matplotlib required. Install: pip install matplotlib")
        except Exception as e:
            print(f"❌ Error creating charts: {str(e)}")
    
    def _is_ranking_data(self, records: List[Dict[str, Any]]) -> bool:
        """Check if data is ranking type"""
        if not records:
            return False
        first = records[0]
        return 'Country' in first and 'GDP' in first
    
    def _is_trend_data(self, records: List[Dict[str, Any]]) -> bool:
        """Check if data is trend type"""
        if not records:
            return False
        first = records[0]
        return 'Year' in first or 'year' in first
    
    def _is_distribution_data(self, records: List[Dict[str, Any]]) -> bool:
        """Check if data is distribution type"""
        if not records:
            return False
        first = records[0]
        return 'Continent' in first and 'Contribution' in first
    
    def _create_bar_chart(self, records: List[Dict[str, Any]]) -> None:
        """Create bar chart"""
        import matplotlib.pyplot as plt
        
        if 'Country' in records[0]:
            labels = [r['Country'] for r in records]
            values = [r['GDP'] for r in records]
            title = 'Countries by GDP'
            ylabel = 'GDP (USD)'
        else:
            labels = [r.get('label', str(i)) for i, r in enumerate(records)]
            values = [list(r.values())[1] for r in records]
            title = 'Data Comparison'
            ylabel = 'Value'
        
        plt.figure(figsize=(12, 6))
        plt.bar(labels, values, color='steelblue', edgecolor='black')
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Category', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        plt.savefig(f'{self.output_dir}/bar_chart.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_line_chart(self, records: List[Dict[str, Any]]) -> None:
        """Create line chart"""
        import matplotlib.pyplot as plt
        
        years = [r.get('Year', r.get('year')) for r in records]
        values = [list(r.values())[1] for r in records]
        
        plt.figure(figsize=(12, 6))
        plt.plot(years, values, marker='o', linewidth=2, markersize=8, color='green')
        plt.title('Trend Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plt.savefig(f'{self.output_dir}/line_chart.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_pie_chart(self, records: List[Dict[str, Any]]) -> None:
        """Create pie chart"""
        import matplotlib.pyplot as plt
        
        labels = [r['Continent'] for r in records]
        values = [r['Contribution'] for r in records]
        
        plt.figure(figsize=(10, 8))
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Distribution', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        plt.savefig(f'{self.output_dir}/pie_chart.png', dpi=300, bbox_inches='tight')
        plt.close()


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
    
    