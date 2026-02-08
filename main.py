from modules.data_loader import load_gdp_data, transform_data
from modules.data_processor import save_long_data

file_path = "gdp_with_continent_filled.csv"
output_file = "gdp_long_format.csv"

raw_data = load_gdp_data(file_path)
long_data = transform_data(raw_data)

save_long_data(long_data, output_file)
print(len(long_data))

print("✅ Long format GDP data saved successfully")