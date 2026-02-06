import os
import sys

def print_header(text):
    #fancy header
    print("\n"+"="*70)
    print(f"{text}")
    print("="*70)

def print_section(text):
    #section title
    print(f"\n{'-'*70}")
    print(f"{text}")
    print(f"{'-'*70}")

def display_config(config):
    #configuration settings
    print_section("CONFIGURATION")
    print(f"\n Continent : {config.get('continent','N/A')}")
    print(f" Year      : {config.get('year','N/A')}")
    print(f" Operation : {config.get('operation','N/A')}")


def display_results(continent,year,operation,result):
    #Display analysis results
    print_section("RESULTS")
    print(f"\n {operation.upper()} GDP for {continent} in {year}:")
    print(f" ${result:,.2f} USD")

def main():
    print_header("GDP ANALYSIS DASHBOARD")

    #importing modules
    try:
        from modules.config_handler import load_config,validate_config
        from modules.data_loader import load_gdp_data,validate_data_structure
        from modules.data_processor import (clean_data,filter_by_continent,perform_operation,get_continent_gdp_data,get_continent_yearly_gdp)
        from modules.visualizer import(pie_chart,bar_chart,line_chart,scatter_chart)
        
        print("Modules loaded")

    except ImportError as e:
        print(f" Error loading modules: {e}")
        print("Make sure files are in modules folder")
        return
    
    try:
       #loading config
       print_section("LOADING DATA")
       config=load_config('config.json')
       validate_config(config)
       print("Config loaded")
    
       #display config
       display_config(config)

       #load and process data
       data=load_gdp_data(config['data_file'])
       validate_data_structure(data)
       cleaned=clean_data(data)
       filtered=filter_by_continent(cleaned,config['continent'])

       #calculate and display results
       result=perform_operation(filtered,config['year'],config['operation'])
       display_results(config['continent'],config['year'],config['operation'],result)

       #visualizations generation
       print_section("GENERATING CHARTS")

       #create folder
       if not os.path.exists('visualizations'):
           os.makedirs('visualizations')

       #get data
       continent_gdp=get_continent_gdp_data(cleaned,config['year'])
       yearly_gdp=get_continent_yearly_gdp(cleaned,config['continent'])

       #charts creation
       print()
       pie_chart(continent_gdp,f"GDP Distribution {config['year']}",'visualizations/continent_pie.png')

       bar_chart(continent_gdp,f"GDP by Continent {config['year']}",'Continent','GDP','visualizations/continent_bar.png')

       line_chart(yearly_gdp,f"GDP Trend - {config['continent']}",'Year','GDP','visualizations/yearly_line.png')

       scatter_chart(yearly_gdp,f"GDP Scatter - {config['continent']}",'Year','GDP','visualizations/yearly_scatter.png')

       print("\n All charts saved in visualizations folder!")
       
       print("\n"+"="*70)
       print("ANALYSIS COMPLETE!")
       print("="*70+"\n")

    except FileNotFoundError as e:
        print(f"\n File not found: {e}")
        print("Make sure config.json and data file exist!")

    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == "__main__":
    main()   