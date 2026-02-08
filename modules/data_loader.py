import csv    # to read CSV files
import os   

def load_gdp_data(file_path):
    """
    Load GDP data from CSV and return raw rows.
    """
   
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}") #kia file exist krti ha?

    # Step 2: Open file and read rows
    try:

        with open(file_path, 'r', encoding='utf-8') as f:
             reader = csv.DictReader(f)
             data = list(reader) 
             # convert CSV into a list of dictionaries
        if not data
                        raise ValueError("CSV file is empty!")
    except Exception as e:
        print("Error reading CSV file:", e)
        raise


        return data
        
def transform_data(raw_data):
    """
    Convert wide format (years as columns) to long format (one row per year)
    """
    long_data = [
        {
            "country": row["\ufeffCountry Name"], #country ka nam le ga
            "continent": row["Continent"], #continent get kary ga
            "year": int(year), #saray years get karay ga
            "value": float(row[year]) if row[year] else 0 #us year k gdp ko float me convert karay ga or agr 
            # gdp empty ha too zero likh do
        }
        for row in raw_data  #raw data me se aik aik row nikaalay gi
        for year in row.keys()  #us rows me se years nikalay gii
        if year.isdigit()  # or agar year digit ho ga to save kre gi
    ]
    return long_data

def clean_long_data(long_data):

    return [row for row in long_data if row["country"] and row["continent"] and row["year"]]