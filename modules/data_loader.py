import csv
import os

def load_gdp_data(file_path):
    """Load GDP data from CSV and return raw rows."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        if not data:
            raise ValueError("CSV file is empty!")
        
        return data
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")

def transform_data(raw_data):
    """Convert wide format (years as columns) to long format (one row per year)."""
    long_data = [
        {
            "country": row.get("Country Name") or row.get("\ufeffCountry Name"),
            "continent": row.get("Continent","Unknown"),
            "year": int(year),
            "value": float(row[year]) if row.get(year) and row[year].strip() else 0
        }
        for row in raw_data
        for year in row.keys()
        if year.isdigit()
    ]
    return long_data

def clean_long_data(long_data):
    """Remove invalid or missing entries."""
    cleaned = [
        row for row in long_data
        if row["country"] and row["continent"] and isinstance(row["year"], int)
           and isinstance(row["value"], (int, float)) and row["value"] >= 0
    ]
    return cleaned
