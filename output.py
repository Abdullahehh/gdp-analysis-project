import json
import csv
import os
from typing import List, Dict, Any

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.visualizer import pie_chart, bar_chart, line_chart, scatter_chart


# =========================================================
# CONSOLE WRITER
# =========================================================

class ConsoleWriter:
    """Displays results in terminal"""

    def write(self, results: Dict[str, Any]) -> None:
        """Write results to console - handles nested dictionary from engine"""
        if not results:
            print("  No data to display")
            return

        print("\n" + "=" * 80)
        print("  RESULTS")
        print("=" * 80)

        if isinstance(results, dict):
            if 'top_10' in results:
                self._print_analysis_results(results)
            else:
                for key, value in results.items():
                    print(f"\n{key}: {value}")
        else:
            for i, record in enumerate(results, 1):
                print(f"\n{i}. ", end="")
                for key, value in record.items():
                    if isinstance(value, float):
                        print(f"{key}: ${value:,.2f}", end="  |  ")
                    else:
                        print(f"{key}: {value}", end="  |  ")
                print()

        print("\n" + "=" * 80 + "\n")

    def _print_analysis_results(self, results: Dict[str, Any]) -> None:

        if 'top_10' in results and results['top_10']:
            print("\n" + "-" * 80)
            print("  OUTPUT 1: TOP 10 COUNTRIES BY GDP")
            print("-" * 80)
            for i, item in enumerate(results['top_10'], 1):
                print(f"  {i}. {item['country']:30s} ${item['gdp']:>15,.2f}")

        if 'bottom_10' in results and results['bottom_10']:
            print("\n" + "-" * 80)
            print("  OUTPUT 2: BOTTOM 10 COUNTRIES BY GDP")
            print("-" * 80)
            for i, item in enumerate(results['bottom_10'], 1):
                print(f"  {i}. {item['country']:30s} ${item['gdp']:>15,.2f}")

        if 'growth_rate' in results and results['growth_rate']:
            print("\n" + "-" * 80)
            print("  OUTPUT 3: GDP GROWTH RATE BY COUNTRY")
            print("-" * 80)
            for country, rate in list(results['growth_rate'].items())[:20]:
                print(f"  {country:30s} {rate:>8.2f}%")

        if 'avg_by_continent' in results and results['avg_by_continent']:
            print("\n" + "-" * 80)
            print("  OUTPUT 4: AVERAGE GDP BY CONTINENT")
            print("-" * 80)
            for continent, avg_gdp in results['avg_by_continent'].items():
                print(f"  {continent:30s} ${avg_gdp:>15,.2f}")

        if 'global_gdp_trend' in results and results['global_gdp_trend']:
            print("\n" + "-" * 80)
            print("  OUTPUT 5: GLOBAL GDP TREND")
            print("-" * 80)
            for year, gdp in list(results['global_gdp_trend'].items())[:5]:
                print(f"  {year}: ${gdp:>15,.2f}")

        if 'fastest_growing' in results:
            print("\n" + "-" * 80)
            print("  OUTPUT 6: FASTEST GROWING CONTINENT")
            print("-" * 80)
            print(f"  {results['fastest_growing']}")

        if 'consistent_decline' in results:
            print("\n" + "-" * 80)
            print("  OUTPUT 7: COUNTRIES WITH CONSISTENT GDP DECLINE")
            print("-" * 80)
            if results['consistent_decline']:
                for country in results['consistent_decline']:
                    print(f"  - {country}")
            else:
                print("  (No countries with consistent decline)")

        if 'continent_contribution' in results and results['continent_contribution']:
            print("\n" + "-" * 80)
            print("  OUTPUT 8: CONTINENT CONTRIBUTION TO GLOBAL GDP")
            print("-" * 80)
            for continent, percentage in results['continent_contribution'].items():
                print(f"  {continent:30s} {percentage:>6.2f}%")


# =========================================================
# GRAPHICS WRITER
# =========================================================

class GraphicsChartWriter:

    def __init__(self, output_dir: str = 'visualizations'):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def write(self, results: Dict[str, Any]) -> None:
        if not results:
            print("  No data to visualize")
            return

        try:
            if isinstance(results, dict) and 'top_10' in results:
                self._create_analysis_charts(results)
            else:
                print("  No compatible data for charts")

            print(f"  Charts saved in {self.output_dir}/")

        except Exception as e:
            print(f"  Error creating charts: {str(e)}")

    def _create_analysis_charts(self, results: Dict[str, Any]) -> None:

        if 'top_10' in results and results['top_10']:
            top_10_dict = {item['country']: item['gdp'] for item in results['top_10']}
            bar_chart(
                top_10_dict,
                'Top 10 Countries by GDP',
                'Country',
                'GDP (USD)',
                os.path.join(self.output_dir, 'top_10_bar.png')
            )

        if 'continent_contribution' in results and results['continent_contribution']:
            pie_chart(
                results['continent_contribution'],
                'Continent Contribution to Global GDP (%)',
                os.path.join(self.output_dir, 'continent_contribution_pie.png')
            )

        if 'global_gdp_trend' in results and results['global_gdp_trend']:
            line_chart(
                results['global_gdp_trend'],
                'Global GDP Trend Over Time',
                'Year',
                'GDP (USD)',
                os.path.join(self.output_dir, 'global_trend_line.png')
            )

        if 'avg_by_continent' in results and results['avg_by_continent']:
            bar_chart(
                results['avg_by_continent'],
                'Average GDP by Continent',
                'Continent',
                'Average GDP (USD)',
                os.path.join(self.output_dir, 'avg_continent_bar.png')
            )


# =========================================================
# FILE WRITER
# =========================================================

class FileWriter:

    def __init__(self, output_path: str, format: str = 'csv'):
        self.output_path = output_path
        self.format = format.lower()

        if self.format not in ['csv', 'json']:
            raise ValueError("Format must be 'csv' or 'json'")

    def write(self, results: Dict[str, Any]) -> None:
        if not results:
            print("  No data to write")
            return

        try:
            if isinstance(results, dict) and 'top_10' in results:
                records = self._flatten_results(results)
            else:
                records = results

            if self.format == 'csv':
                self._write_csv(records)
            else:
                self._write_json(records)

            print(f"  Data saved to {self.output_path}")

        except Exception as e:
            print(f"  Error writing file: {str(e)}")

    def _write_csv(self, records: List[Dict[str, Any]]) -> None:
        with open(self.output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    def _write_json(self, records: List[Dict[str, Any]]) -> None:
        with open(self.output_path, 'w', encoding='utf-8') as file:
            json.dump(records, file, indent=2, ensure_ascii=False)

    def _flatten_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        flattened = []

        if 'top_10' in results:
            for item in results['top_10']:
                flattened.append({
                    'Analysis': 'Top 10',
                    'Country': item['country'],
                    'GDP': item['gdp']
                })

        if 'bottom_10' in results:
            for item in results['bottom_10']:
                flattened.append({
                    'Analysis': 'Bottom 10',
                    'Country': item['country'],
                    'GDP': item['gdp']
                })

        if 'growth_rate' in results:
            for country, rate in results['growth_rate'].items():
                flattened.append({
                    'Analysis': 'Growth Rate',
                    'Country': country,
                    'Growth_Rate_%': rate
                })

        if 'avg_by_continent' in results:
            for continent, avg in results['avg_by_continent'].items():
                flattened.append({
                    'Analysis': 'Average by Continent',
                    'Continent': continent,
                    'Average_GDP': avg
                })

        return flattened if flattened else [results]


# =========================================================
# HTML REPORT WRITER
# =========================================================

class HTMLReportWriter:

    def __init__(self, output_path: str = 'report.html'):
        self.output_path = output_path

    def write(self, results: Dict[str, Any]) -> None:
        if not results:
            print("  No data to write")
            return

        try:
            if isinstance(results, dict) and 'top_10' in results:
                html = self._generate_analysis_html(results)
            else:
                html = "<html><body><h1>No compatible data</h1></body></html>"

            with open(self.output_path, 'w', encoding='utf-8') as file:
                file.write(html)

            print(f"  HTML report saved to {self.output_path}")

        except Exception as e:
            print(f"  Error creating HTML report: {str(e)}")

    def _generate_analysis_html(self, results: Dict[str, Any]) -> str:

        html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>GDP Analysis Report - Phase 2</title>
<style>
body { font-family: Arial; margin: 40px; background: #f5f5f5; }
h1 { text-align: center; }
table { width: 100%; border-collapse: collapse; background: white; }
th { background: #4CAF50; color: white; padding: 10px; }
td { padding: 8px; border-bottom: 1px solid #ddd; }
</style>
</head>
<body>
<h1>GDP Analysis Report - Phase 2</h1>
"""

        if 'top_10' in results:
            html += "<h2>Top 10 Countries</h2><table><tr><th>Rank</th><th>Country</th><th>GDP</th></tr>"
            for i, item in enumerate(results['top_10'], 1):
                html += f"<tr><td>{i}</td><td>{item['country']}</td><td>${item['gdp']:,.2f}</td></tr>"
            html += "</table>"

        html += "</body></html>"
        return html