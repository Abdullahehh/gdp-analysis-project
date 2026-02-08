def save_long_data(long_data, output_file):
    import csv
    if not long_data:
        raise ValueError("No data to save.")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=long_data[0].keys())
        writer.writeheader()
        writer.writerows(long_data)

def filter_data(long_data, config):
 
    region_input = config["region"].strip().lower()
    year = int(config["year"])
    country = config.get("country")
    if country:
        country = country.strip().lower()
    
    # Parse multiple regions
    if '&' in region_input:
        regions = [r.strip() for r in region_input.split('&')]
    elif ',' in region_input:
        regions = [r.strip() for r in region_input.split(',')]
    else:
        regions = [region_input]
    
    print(f"\nFiltering for: regions={regions}, year={year}", end="")
    if country:
        print(f", country={country}")
    else:
        print(" (all countries)")
    
    filtered = list(filter(
        lambda x: (
            x["continent"] and x["continent"].strip().lower() in regions and
            x["year"] == year and
            (country is None or (x["country"] and x["country"].strip().lower() == country))
        ),
        long_data
    ))
    
    print(f"Found {len(filtered)} matching records")
    return filtered
    
def compute_stat(filtered_data, operation):
 
    if not filtered_data:
        return 0.0
    
    values = [x["value"] for x in filtered_data if isinstance(x["value"], (int, float))]
    
    if not values:
        return 0.0
    
    if operation == "average":
        if len(values) == 0:
            return 0.0
        return sum(values) / len(values)
    elif operation == "sum":
        return sum(values)
    else:
        raise ValueError(f"Invalid operation: {operation}")