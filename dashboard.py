import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from config_handler import load_config, validate_config
from data_loader import load_gdp_data, transform_data, clean_long_data
from data_processor import save_long_data, filter_data, compute_stat
from visualizer import pie_chart, bar_chart, line_chart, scatter_chart

def print_header(text):
    print("\n"+"="*70)
    print(f"{text}")
    print("="*70)

def print_section(text):
    print(f"\n{'-'*70}")
    print(f"{text}")
    print(f"{'-'*70}")

def display_config(config):
    print_section("CONFIGURATION")
    print(f"\n Region  : {config.get('region','N/A')}")
    print(f" Year    : {config.get('year','N/A')}")
    print(f" Operation : {config.get('operation','N/A')}")
    print(f" Country : {config.get('country','All')}")

def display_results(region, year, operation, result):
    print_section("RESULTS")
    print(f"\n {operation.upper()} GDP for {region} in {year}:")
    print(f" ${result:,.2f} USD")

def main():
    print_header("GDP ANALYSIS DASHBOARD")

    try:
        # Load configuration
        print_section("LOADING CONFIGURATION")
        config = load_config("config.json")
        is_valid, message = validate_config(config)
        if not is_valid:
            print(f"Configuration Error: {message}")
            sys.exit(1)
        print("Config loaded successfully")
        display_config(config)

        # Load and process data
        print_section("LOADING DATA")
        raw_data = load_gdp_data(config.get("data_file","gdp_with_continent_filled.csv"))
        long_data = transform_data(raw_data)
        long_data = clean_long_data(long_data)
        print(f" Total records after cleaning: {len(long_data)}")

        #save long format
        save_long_data(long_data, "gdp_long_format.csv")
        print(" Long format GDP data saved to gdp_long_format.csv")

        # Filter and compute
        filtered = filter_data(long_data, config)
        result = compute_stat(filtered, config["operation"])
        display_results(config["region"], config["year"], config["operation"], result)

       # Generate visualizations
        print_section("GENERATING CHARTS")
        if not os.path.exists('visualizations'):
            os.makedirs('visualizations')

        # Data for charts
        # Pie/Bar: region-wise GDP for selected year
        region_data = {}
        for row in filter(lambda x: x["year"] == config["year"], long_data):
            key = row["continent"]
            region_data[key] = region_data.get(key, 0) + row["value"]

        # FIXED: Line/Scatter - handle multiple regions
        config_region_lower = config["region"].strip().lower()

        # Parse multiple regions
        if '&' in config_region_lower:
            regions = [r.strip() for r in config_region_lower.split('&')]
        elif ',' in config_region_lower:
            regions = [r.strip() for r in config_region_lower.split(',')]
        else:
            regions = [config_region_lower]

        # Collect trend data for all specified regions
        trend_data = {}
        for row in long_data:
            if row["continent"] and row["continent"].strip().lower() in regions:
                trend_data[row["year"]] = trend_data.get(row["year"], 0) + row["value"]

        # Add validation before creating charts
        if not region_data:
            print("⚠️  Warning: No regional data available for charts")
        else:
            pie_chart(region_data, f"GDP Distribution {config['year']}", 
                    'visualizations/continent_pie.png')
            bar_chart(region_data, f"GDP by Region {config['year']}", 
                    'Region', 'GDP (USD)', 'visualizations/continent_bar.png')

        if not trend_data:
            print(f"⚠️  Warning: No trend data available for {config['region']}")
        else:
            chart_title = f"GDP Trend - {config['region']}"
            line_chart(trend_data, chart_title, 
                    'Year', 'GDP (USD)', 'visualizations/yearly_line.png')
            scatter_chart(trend_data, chart_title, 
                        'Year', 'GDP (USD)', 'visualizations/yearly_scatter.png')

        print("\n✅ All charts saved in visualizations folder!")
        print("\n"+"="*70)
        print("ANALYSIS COMPLETE!")
        print("="*70+"\n")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
