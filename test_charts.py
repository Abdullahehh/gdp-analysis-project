
import os
from modules.visualizer import *

# Create visualizations folder if it doesn't exist
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

# Test data
test_continents = {
    'Asia': 25000000000,
    'Europe': 18000000000,
    'Africa': 3000000000,
    'North America': 22000000000
}

test_years = {
    2015: 20000000000,
    2016: 21000000000,
    2017: 22500000000,
    2018: 24000000000,
    2019: 25000000000,
    2020: 23000000000
}

print("Testing your visualizer...")
print()

pie_chart(test_continents, "Test Pie Chart - GDP by Continent", "visualizations/test_pie.png")
bar_chart(test_continents, "Test Bar Chart - GDP Comparison", "Continent", "GDP (USD)", "visualizations/test_bar.png")
line_chart(test_years, "Test Line Chart - GDP Trend", "Year", "GDP (USD)", "visualizations/test_line.png")
scatter_chart(test_years, "Test Scatter Chart - GDP Analysis", "Year", "GDP (USD)", "visualizations/test_scatter.png")

print()
print("=" * 60)
print("SUCCESS!")
print("=" * 60)