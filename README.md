# 🌍 GDP Analysis System - Phase 1

## Project Overview
A comprehensive GDP data analysis system that processes World Bank GDP data and generates professional visualizations using functional programming principles in Python.

## 👥 Team Members
- **MINAHIL MIRZA** - Data Processing , Loading & Core Logic Implementation
- **ABDULLAH JAVAID** - Visualization Module & Dashboard Development

## 📋 Project Description
This system analyzes World Bank GDP data by:
- Loading and cleaning GDP datasets from Excel files
- Filtering data by continent, year, and country
- Performing statistical operations (average, sum)
- Generating multiple types of professional visualizations
- Operating entirely through configuration files (no hardcoded values)

## ✨ Key Features
- ✅ **Configuration-Driven**: All parameters controlled via `config.json`
- ✅ **Functional Programming**: Uses map, filter, lambda, and comprehensions
- ✅ **Multiple Visualizations**: Pie charts, bar charts, line graphs, scatter plots
- ✅ **Single Responsibility Principle**: Clean modular architecture
- ✅ **Error Handling**: Comprehensive validation and error messages
- ✅ **Professional Output**: High-resolution charts (300 DPI)

## 🛠️ Technology Stack
- **Language**: Python 3.8+
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib
- **File Handling**: openpyxl (for Excel files)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/Abdullahehh/gdp-analysis-project.git
cd gdp-analysis-project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python --version
# Should show Python 3.8 or higher
```

## 🚀 Usage

### Basic Usage
1. **Configure your analysis** by editing `config.json`:
```json
{
  "data_file": "data/gdp_data.xlsx",
  "continent": "Asia",
  "year": 2020,
  "country": "Pakistan",
  "operation": "average"
}
```

2. **Run the dashboard**:
```bash
python dashboard.py
```

3. **View results**:
   - Console displays statistical analysis
   - Charts saved in `visualizations/` folder

### Configuration Options

#### `config.json` Parameters:
- **data_file**: Path to GDP data Excel file
- **continent**: Target continent for analysis
  - Options: Asia, Europe, Africa, North America, South America, Oceania
- **year**: Year to analyze (1960-2024)
- **country**: Specific country for detailed analysis
- **operation**: Statistical operation to perform
  - Options: `average` or `sum`

### Example Configurations

**Analyze European GDP in 2019:**
```json
{
  "continent": "Europe",
  "year": 2019,
  "operation": "sum"
}
```

**Calculate average GDP for Africa in 2020:**
```json
{
  "continent": "Africa",
  "year": 2020,
  "operation": "average"
}
```

## 📁 Project Structure
```
gdp-analysis-project/
├── dashboard.py                 # Main program entry point
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
│
├── data/
│   └── gdp_data.xlsx           # GDP dataset
│
├── modules/
│   ├── config_handler.py       # Configuration management
│   ├── data_loader.py          # Data loading functions
│   ├── data_processor.py       # Data processing & filtering
│   └── visualizer.py           # Chart generation
│
└── visualizations/             # Generated charts (created on run)
    ├── continent_gdp_pie.png
    ├── continent_gdp_bar.png
    ├── yearly_gdp_line.png
    └── yearly_gdp_scatter.png
```

## 📊 Output

### Console Output
The dashboard displays:
- Configuration settings
- Dataset information (total countries, continents)
- Statistical results (average/sum GDP)
- Visualization generation status

### Generated Visualizations
All charts saved in `visualizations/` folder:

1. **continent_gdp_pie.png**
   - Pie chart showing GDP distribution by continent
   - Displays percentages for each continent

2. **continent_gdp_bar.png**
   - Bar chart comparing GDP across continents
   - Includes value labels on each bar

3. **yearly_gdp_line.png**
   - Line chart showing GDP trends over years
   - Displays historical GDP progression

4. **yearly_gdp_scatter.png**
   - Scatter plot with trend line
   - Shows GDP correlation over time

## 🔧 Module Details

### `config_handler.py` (by Partner)
Manages configuration from `config.json`
- Loads and parses JSON configuration
- Validates all parameters
- Provides error messages for invalid configs

### `data_loader.py` (by Partner)
Handles data file operations
- Loads Excel and CSV files
- Validates data structure
- Provides dataset information

### `data_processor.py` (by Partner)
Processes and analyzes GDP data using functional programming
- Cleans data (handles missing values)
- Filters by continent, year, country
- Calculates statistics (average, sum)
- Prepares data for visualization
- Uses map, filter, lambda, comprehensions

### `visualizer.py` (by Me)
Creates professional visualizations
- Generates 4 types of charts
- Handles styling and formatting
- Exports high-resolution PNG files

## 🎓 Functional Programming Implementation

This project demonstrates functional programming through:

### List Comprehensions
```python
# Filter missing fields
missing_fields = [field for field in required_fields if field not in config]
```

### Dictionary Comprehensions
```python
# Aggregate GDP by continent
continent_gdp = {
    continent: calculate_sum_gdp(data, year)
    for continent in continents
}
```

### Set Comprehensions
```python
# Get unique continents
continents = {cont for cont in data['Continent'] if cont != ''}
```

### map() Function
```python
# Convert values to float
total = sum(map(lambda x: float(x), gdp_values))
```

### filter() Function
```python
# Filter positive GDP values
gdp_values = list(filter(lambda x: x > 0, data[year].values))
```

### lambda Expressions
```python
# Apply data cleaning
cleaned_data[year_columns].apply(lambda col: col.fillna(0))
```

## 🧪 Testing

### Test Your Installation
```bash
# Run a test with sample data
python test_charts.py
```

### Expected Output
- Console shows success messages
- 4 PNG files created in `visualizations/`

### Verify Charts
1. Navigate to `visualizations/` folder
2. Open PNG files to verify chart quality
3. Check that all labels and titles are correct

## 🆘 Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "File not found: config.json"
**Solution:**
- Ensure `config.json` exists in project root
- Check file spelling and location

### Issue: "Data file not found"
**Solution:**
- Verify `gdp_data.xlsx` is in `data/` folder
- Check `data_file` path in `config.json`

### Issue: "No visualizations created"
**Solution:**
- Check console for error messages
- Verify matplotlib is installed: `pip install matplotlib`
- Ensure `visualizations/` folder exists (created automatically)

### Issue: "Invalid configuration"
**Solution:**
- Check `config.json` syntax (valid JSON)
- Verify year is between 1960-2024
- Ensure operation is "average" or "sum"

## 📚 Dependencies

### Core Libraries
- **pandas (>=2.0.0)**: Data manipulation and analysis
- **matplotlib (>=3.7.0)**: Chart generation and visualization
- **numpy (>=1.24.0)**: Numerical computations
- **openpyxl (>=3.1.0)**: Excel file support

### Installation
All dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 🎨 Design Principles

### Single Responsibility Principle (SRP)
Each module has one clear purpose:
- **config_handler**: Only manages configuration
- **data_loader**: Only loads data
- **data_processor**: Only processes data
- **visualizer**: Only creates visualizations
- **dashboard**: Only orchestrates the system

### Configuration-Driven Design
- All analysis parameters in `config.json`
- No hardcoded values in source code
- Easy to modify without code changes

### Error Handling
- Validates configuration before use
- Checks data structure
- Provides meaningful error messages
- Graceful failure handling

## 📈 Performance

### Typical Performance
- Load data: ~1-2 seconds
- Process data: ~0.5-1 second
- Generate visualizations: ~2-3 seconds
- **Total execution time**: ~5-7 seconds

### Scalability
- Handles datasets with 200+ countries
- Processes 60+ years of data efficiently
- Generates high-resolution charts quickly

## 🔮 Future Enhancements

Potential improvements for future versions:
- Interactive web-based dashboard
- Additional chart types (heatmaps, treemaps)
- Export results to PDF reports
- Support for multiple countries comparison
- Time-series forecasting
- Database integration
- Real-time data updates

## 📄 License
Academic project for Software Development & Analysis course.

## 🙏 Acknowledgments
- World Bank for GDP data
- SDA Course Instructors
- Python community for excellent libraries
- Project partner for collaboration

## 📞 Contact

### Project Team
- **Abdullah Javaid**
  - Email: [abdullahjavaidaries2022@gmail.com]
  - GitHub: [Abdullahehh](https://github.com/Abdullahehh)
  
- **Minahil Mirza**
  - Email: [minahilmirza948@gmail.com]
  - GitHub: [minahil948](https://github.com/minahil948)

### Repository
- GitHub: [https://github.com/Abdullahehh/gdp-analysis-project](https://github.com/Abdullahehh/gdp-analysis-project)

