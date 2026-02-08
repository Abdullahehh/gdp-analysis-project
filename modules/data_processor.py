def save_long_data(long_data, output_file):
    import csv
    if not long_data:
        raise ValueError("No data to save.")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=long_data[0].keys())
        writer.writeheader()
        writer.writerows(long_data)

def filter_data(long_data, config):
    """
    Filter data based on region, year, and optionally country.
    Case-insensitive and trims extra spaces for robust matching.
    """
    region = config["region"].strip().lower()
    year = int(config["year"])
    country = config.get("country")
    if country:
        country = country.strip().lower()
    
 
    print(f"\nFiltering for: region='{region}', year={year}, country={country}")
    
    filtered = list(filter(
        lambda x: (
            x["continent"] and region in x["continent"].strip().lower() and  # Changed to 'in' instead of '=='
            x["year"] == year and
            (country is None or (x["country"] and x["country"].strip().lower() == country))
        ),
        long_data
    ))
    
    print(f"Found {len(filtered)} matching records")
    return filtered
    
def compute_stat(filtered_data, operation):
    """
    Compute sum or average of GDP values safely.
    Returns 0 if no data is present.
    """
    if not filtered_data:
        return 0.0
    
    values = [x["value"] for x in filtered_data if isinstance(x["value"], (int, float))]
    
    if not values:
        return 0.0
    
    if operation == "average":
        return sum(values) / len(values)
    elif operation == "sum":
        return sum(values)
    else:
        raise ValueError(f"Invalid operation: {operation}")