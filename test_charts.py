import os
from modules.visualizer import *

if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

continents = {
    'Asia': 25000000000,
    'Europe': 18000000000,
    'Africa': 3000000000
}

years = {
    2015: 20000000000,
    2017: 22000000000,
    2019: 24000000000,
    2021: 26000000000
}

# Test charts
print("Testing visualizer...")
pie_chart(continents, "Test Pie", "visualizations/test_pie.png")
bar_chart(continents, "Test Bar", "Continent", "GDP", "visualizations/test_bar.png")
line_chart(years, "Test Line", "Year", "GDP", "visualizations/test_line.png")
scatter_chart(years, "Test Scatter", "Year", "GDP", "visualizations/test_scatter.png")
print("\n All charts passed!")