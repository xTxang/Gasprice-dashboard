# Outputs a table showing the gas deposits in all EU countries, including the % fill, how much to fill, days until deadline


import csv
import os
import requests
from datetime import datetime
import pandas as pd

# for testing purposes, not production
import pprint




# --- SETTINGS ---
API_KEY = "d9c96ee569ffd1dacbd77404a468c5dc"
DOWNLOAD_FOLDER = "agsi-country-files"
FILENAME = f"agsi_country_data_{datetime.today().strftime('%Y-%m-%d')}.csv"


# check if folder exists, if not creates it:
file_path = r"C:\users\willi\OneDrive\Documents\GitHub\Gasprice-dashboard\agsi-country-files"
if not os.path.exists(file_path):
    print("Files directory not found, creating...")
    os.makedirs("agsi-country-files")
    


# Request an up to date file:
headers = {
    "x-key": API_KEY
}


# Data is returned as json
response = requests.get("https://agsi.gie.eu/api", headers=headers)

data = response.json()


# pprint.pprint(data)


# --- HELPER FUNCTION ---
def safe_float(value, default=0.0):
    """
    Tries to convert a value to a float. If it fails, it returns a default value.
    This handles non-numeric API responses like '-'.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default



# gets the date from the returned data
filedate = data.get("gas_day")


# Retrieves country level storage, with a dictionary per country
countries = data["data"]


# Parse data into a a dataframe
records = []
# The 'data' key contains a list of top-level groups (e.g., EU, Non-EU).
top_level_groups = data.get("data", [])



for group in top_level_groups:
    countries_in_group = group.get("children", [])
    for country in countries_in_group:
        # Use the safe_float function for all numerical conversions
        records.append({
            "Date": filedate,
            "Country": country.get("name"),
            "Gas in Storage (TWh)": safe_float(country.get("gasInStorage")),
            "Working Gas Capacity (TWh)": safe_float(country.get("workingGasVolume")),
            "Full (%)": safe_float(country.get("full")),
            "Trend (%)": safe_float(country.get("trend")),
            "Consumption (TWh)": safe_float(country.get("consumption"))
        })
# save to CSV
df = pd.DataFrame(records)

output_path = os.path.join(file_path, FILENAME)
df.to_csv(output_path, index=False)
print(f"CSV file saved to: {file_path}")



def display_file_summary(output_path):
    days_until_deadline = 0
    data = []
    with open(output_path, 'r',newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            try:
                if days_until_deadline == 0:
                    date_from_data = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                    deadline_date = datetime(2025, 10, 1).date()
                    time_difference = deadline_date - date_from_data
                    days_until_deadline = time_difference.days
                    country_entry = {'Country': row['Country'], 'Gas in Storage(TWh)': float(row['Gas in Storage (TWh)']), 'Full %': float(row['Full (%)']), 'Gap': (((float(row['Gas in Storage (TWh)'])/float(row['Full (%)']))*100)-float(row['Gas in Storage (TWh)'])), "deadline": days_until_deadline}
                else:
                    country_entry = {'Country': row['Country'], 'Gas in Storage(TWh)': float(row['Gas in Storage (TWh)']), 'Full %': float(row['Full (%)']), 'Gap': (((float(row['Gas in Storage (TWh)'])/float(row['Full (%)']))*100)-float(row['Gas in Storage (TWh)'])), "deadline": days_until_deadline}
            except ZeroDivisionError:
                country_entry = {'Country': row['Country'], 'Gas in Storage(TWh)': float(row['Gas in Storage (TWh)']), 'Full %': float(row['Full (%)']), 'Gap': 0, "deadline": days_until_deadline}




            data.append(country_entry)

            
    # 2. Convert your data into a pandas DataFrame.
    df = pd.DataFrame(data)

    # 3. Specify the output filename.
    output_filename = 'test.xlsx'

    # 4. Write the DataFrame to an Excel file.
    # The `index=False` argument prevents pandas from writing the DataFrame index as a column.
    df.to_excel(output_filename, index=False)

    print(f"Data successfully saved to {output_filename}")




choice = int(input("Press 1 to view the output of the file."))
if choice == 1:
    # File will be outputted as a .xlxs file for now
    display_file_summary(output_path)



    






# Country - Gas in storage(TWh) - Full(%) - Gap(TWh the amount of gas until full) - days until october 1st









# Parse data into a CSV file:





# FILL PERCENTAGE

# GAP - WORK THIS OUT

# NUMBER OF DAYS UNTIL OCTOBER





# FIND ANY DATA THAT IS MAYBE USEFUL TO A SUPPLY AND DEMAND MODEL