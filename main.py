from modules.data_loader import load_gdp_data, transform_data, clean_long_data
from modules.data_processor import save_long_data,filter_data,compute_stat

file_path = "gdp_with_continent_filled.csv"
output_file = "gdp_long_format.csv"
config_file = "config.json"

raw_data = load_gdp_data(file_path)
long_data = transform_data(raw_data)
long_data = clean_long_data(long_data)


save_long_data(long_data, output_file)


print("✅ Long format GDP data saved successfully")
print(len(long_data))

import json

with open("config.json", "r") as f:
    config = json.load(f)

filtered_data = filter_data(long_data, config)
computing_operations=compute_stat(filtered_data,config["operation"])

print("\nGDP Analysis Result")
print(f"Region : {config['region']}")
print(f"Year   : {config['year']}")
if config["country"]:
    print(f"Country: {config['country']}")
print(f"Operation: {config['operation'].capitalize()}")
print(f"Result   : {computing_operations:,.2f}")  # Comma + 2 decimal points
print("-------------\n")