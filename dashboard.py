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

if __name__ == "__main__":
    main()   