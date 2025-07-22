import requests, pathlib
from datetime import datetime, timedelta, date
import os
import requests
import pathlib
from pathlib import Path
import csv

import re
import os


from tabulate import tabulate

import pandas as pd



# imports the point category map:
from point_category_map import POINT_CATEGORY_MAP


def banner():
    print("")


def retrieve_info(type):
    if type == 'default':
        pass
    elif type == 'custom':
        fromDate = input("Input the start date")
        toDate = input("Input the end date")
        indicator = input("Input indicator(idk what this is lmao)")
        periodType = input("Input period type")
        timezone = input("Input timezone(CET default)")

        retrieve_file(fromDate,toDate,indicator,periodType,timezone)

        pass


def retrieve_file(type='Custom',fromDate=None, toDate=None, indicator=None, periodType=None, timezone=None):
    base = "https://transparency.entsog.eu/api/v1/operationalData.csv"


    if type != 'Custom':


        # Currently sets parameters as the past 7 days
        today = datetime.now()
        to_date   = today.strftime("%Y-%m-%d")
        from_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        

        # Customisable parameters
        params = {
            "forceDownload": "true",
            "from": from_date,
            "to": to_date,
            "indicator": "Physical Flow",
            "periodType": "day",
            "timezone": "CET",
            "limit": "-1",
            "dataset": "1",
            "directDownload": "true",
        }
    
    else:
        # Customisable parameters
        params = {
            "forceDownload": "true",
            "from": fromDate,
            "to": toDate,
            "indicator": indicator,
            "periodType": periodType,
            "timezone": timezone,
            "limit": "-1",
            "dataset": "1",
            "directDownload": "true",
        }

        # Ensure the 'files' directory exists
    files_dir = Path("files")
    files_dir.mkdir(parents=True, exist_ok=True)

    # Now safely define the destination file path
    dest = files_dir / f"operationalData_{to_date}.csv"

    try:
        r = requests.get(base, params=params, timeout=60)
        r.raise_for_status()              # will raise if HTTP 4xx/5xx
        dest.write_bytes(r.content)       # plain‑text CSV
        print(f"Saved to {dest.resolve()}")
    except Exception as e:
        print("error :(")



def output_file_summary(chosen_file):
    data = []
    misc_entries = 0  # Makes note of national supplies etc
    malformed_rows = 0
    
    # Extract date from filename
    filename = os.path.basename(chosen_file)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if not date_match:
        print(f"Could not extract date from filename: {filename}")
        return
    
    file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
    print(f"Processing file for date: {file_date}")
    
    with open(chosen_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Skip rows with empty values
                if not row.get('value') or row['value'].strip() == '':
                    malformed_rows += 1
                    continue
                
                point = row['pointLabel'].strip()
                direction = row['directionKey'].strip().lower()
                category = POINT_CATEGORY_MAP.get((point, direction))
                
                if not category:
                    misc_entries += 1
                    continue
                    
                date = datetime.strptime(row['periodTo'], "%Y-%m-%d %H:%M").date()
                value_kwh = float(row['value'])
                value_mcm = value_kwh * 0.000000094  # Converts kWh to mcm
                
                data.append({
                    'date': date,
                    'category': category,
                    'value_mcm': value_mcm,
                    'point': point,
                    'direction': direction
                })
                
            except (KeyError, ValueError) as e:
                malformed_rows += 1
                continue
    
    # Step 3: Load into DataFrame
    df = pd.DataFrame(data)
    if df.empty:
        print("No matching data found.")
        print(f"Miscellaneous entries not categorized: {misc_entries}")
        print(f"Malformed/empty rows: {malformed_rows}")
        return
    
    print(f"Found {len(df)} valid data points")
    print(f"Date range in data: {df['date'].min()} to {df['date'].max()}")
    print(f"Categories found: {df['category'].unique()}")
    
    # Step 4: Aggregate
    daily_totals = df.groupby(['date', 'category'])['value_mcm'].sum().reset_index()
    
    # Step 5: Compute metrics using file date as "today"
    today_date = file_date
    yesterday = today_date - timedelta(days=1)
    week_ago = today_date - timedelta(days=7)
    
    print(f"\nAnalyzing:")
    print(f"Today (from filename): {today_date}")
    print(f"Yesterday: {yesterday}")
    print(f"Week ago: {week_ago}")
    
    summary = []
    for category in daily_totals['category'].unique():
        today_val = daily_totals[
            (daily_totals['date'] == today_date) & 
            (daily_totals['category'] == category)
        ]['value_mcm'].sum()
        
        yest_val = daily_totals[
            (daily_totals['date'] == yesterday) & 
            (daily_totals['category'] == category)
        ]['value_mcm'].sum()
        
        # 7-day average (including today)
        week_data = daily_totals[
            (daily_totals['date'] > week_ago) & 
            (daily_totals['date'] <= today_date) & 
            (daily_totals['category'] == category)
        ]['value_mcm']
        
        last_7d_avg = week_data.mean() if not week_data.empty else 0
        
        delta_yest = ((today_val - yest_val) / yest_val * 100) if yest_val > 0 else None
        delta_7d = ((today_val - last_7d_avg) / last_7d_avg * 100) if last_7d_avg > 0 else None
        
        summary.append([
            category,
            round(today_val, 2),
            f"{delta_yest:+.1f}%" if delta_yest is not None else "N/A",
            f"{delta_7d:+.1f}%" if delta_7d is not None else "N/A"
        ])
    
    # Step 6: Print summary
    print(f"\nGas Flow Summary for {today_date} (mcm/d):")
    print(f"Miscellaneous entries not categorized: {misc_entries}")
    print(f"Malformed/empty rows: {malformed_rows}")
    print(tabulate(summary, headers=['Category', 'Today', 'Δ vs Yesterday', 'Δ vs 7d Avg'], tablefmt='grid'))


# import csv
# import pandas as pd
# from datetime import datetime, timedelta
# from tabulate import tabulate

# def output_file_summary(chosen_file):
#     # Load file
#     df = pd.read_csv(chosen_file)

#     # Filter for Physical Flow rows
#     df = df[df['indicator'] == 'Physical Flow']

#     # Parse datetime
#     df['periodFrom'] = pd.to_datetime(df['periodFrom'], errors='coerce')
#     df['periodTo'] = pd.to_datetime(df['periodTo'], errors='coerce')
#     df['date'] = df['periodTo'].dt.date
#     df['value'] = pd.to_numeric(df['value'], errors='coerce')

#     # Convert kWh/d to mcm/d: 1 kWh ≈ 0.000000094 mcm
#     df['value_mcm'] = df['value'] * 0.000000094

#     # Define PointLabel → Category mapping (expand as needed)
#     point_map = {
#         # NWELNG
#         'Inkoo LNG (FI)': 'NWELNG Send‑Outs',
#         'Zeebrugge IZT': 'NWELNG Send‑Outs',
#         'Gate LNG Terminal (NL)': 'NWELNG Send‑Outs',
#         'Dunkirk (FR)': 'NWELNG Send‑Outs',
#         'Isle of Grain': 'NWELNG Send‑Outs',

#         # Russian
#         'Negru Voda II': 'Russian Pipeline',
#         'Negru Voda III': 'Russian Pipeline',
#         'Isaccea (RO) - Orlovka (UA) II': 'Russian Pipeline',
#         'Isaccea (RO) - Orlovka (UA) III': 'Russian Pipeline',
#         'Nord Stream 1': 'Russian Pipeline',
#         'Yamal–Europe (Poland)': 'Russian Pipeline',

#         # Norwegian
#         'Emden (Norway entry)': 'Norwegian Production',
#         'Zeebrugge (NO)': 'Norwegian Production',
#         'Dunkerque (NO)': 'Norwegian Production',

#         # UK
#         'Bacton': 'UK Production',
#         'St. Fergus': 'UK Production',
#         'Teesside': 'UK Production',

#         # North African
#         'Tarvisio (IT) / Arnoldstein (AT)': 'North African Pipelines',
#         'Trans-Med': 'North African Pipelines',
#         'Medgaz (DZ→ES)': 'North African Pipelines',
#         'GME (LY→IT)': 'North African Pipelines',

#         # TAP
#         'TAP (GR→IT)': 'TAP (Azerbaijan→EU)',
#         'Greece–Italy interconnector': 'TAP (Azerbaijan→EU)',
#     }

#     # Assign categories
#     df['category'] = df.apply(
#         lambda row: point_map.get(row['pointLabel'], None)
#         if row['directionKey'] in ['entry', 'exit'] else None,
#         axis=1
#     )
#     df = df[df['category'].notnull()]

#     # Aggregate mcm/d by (date, category)
#     daily = df.groupby(['date', 'category'])['value_mcm'].sum().reset_index()

#     # Determine latest date
#     latest_date = daily['date'].max()
#     yesterday = latest_date - timedelta(days=1)
#     week_ago = latest_date - timedelta(days=7)

#     summary_rows = []
#     categories = daily['category'].unique()

#     for cat in categories:
#         today_val = daily[(daily['date'] == latest_date) & (daily['category'] == cat)]['value_mcm'].sum()
#         yest_val = daily[(daily['date'] == yesterday) & (daily['category'] == cat)]['value_mcm'].sum()
#         last_7d_avg = daily[(daily['date'] > week_ago) & (daily['date'] <= latest_date) & (daily['category'] == cat)]['value_mcm'].mean()

#         delta_yest = ((today_val - yest_val) / yest_val * 100) if yest_val else None
#         delta_7d = ((today_val - last_7d_avg) / last_7d_avg * 100) if last_7d_avg else None

#         summary_rows.append([
#             cat,
#             round(today_val, 2),
#             f"{delta_yest:+.1f}%" if delta_yest is not None else "N/A",
#             f"{delta_7d:+.1f}%" if delta_7d is not None else "N/A"
#         ])

#     print("\nGAS FLOW SUMMARY (mcm/d)")
#     print(f"For: {latest_date}")
#     print(tabulate(summary_rows, headers=['Category', 'Today (mcm/d)', 'Δ vs Yesterday', 'Δ vs 7d Avg'], tablefmt='grid'))

        





def view_file():
    file_path = r"C:\users\willi\OneDrive\Documents\GitHub\Gasprice-dashboard\files"

    # Check if the files directory exists
    if not os.path.exists(file_path):
        print("Files directory not found!")
        return

    # get all the files in the directory
    files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    


    print("Pick from one of the following:")

    for i, file in enumerate(files):
        print(f"{i+1}. {file}")

    choice = int(input("\nEnter the number of the file you want to view: ")) - 1
    if choice >= 0 and choice < len(files):
        chosen_file = os.path.join(file_path, files[choice])


    

    output_file_summary(chosen_file)

    return chosen_file


    # with open(chosen_file, 'r', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
            
    #     # Fields to display
    #     fields_to_show = ['periodFrom', 'periodType', 'pointLabel', 'directionKey', 'indicator', 'value', 'unit']

    #     table_data = []
    #     for row in reader:
    #         # Extract required fields
    #         filtered_row = [row.get(field, 'N/A') for field in fields_to_show]
    #         table_data.append(filtered_row)
        
    #     # Create headers
    #     headers = ['Period From', 'Period Type', 'Point Label', 'Direction Key', 'Indicator', 'Value', 'Unit']
        
    #     # Display table
    #     print(f"\n{'-'*80}")
    #     print("GAS FLOW DATA TABLE")
    #     print(f"{'-'*80}")
    #     print(tabulate(table_data, headers=headers, tablefmt='grid'))
    #     print(f"\nTotal records: {len(table_data)}")
        

    



def main_menu():
    while True:
        print("\n===== MAIN MENU =====")
        banner()
        print("1. Run For today")
        print("2. Custom Run")
        print("3. View file")



        choice = input("\nEnter your choice")
        if choice == '1':
            retrieve_file(type='default')
        elif choice == '2':
            retrieve_info('custom') 
        elif choice == '3':
            file_dash()







        


        # viewing

        # default view : indicator, pointlabel, tsoidentifier

        # custom view





def file_dash():
    # have date filters on the files 
    # display the files is already done
    # categorise into the pointlabel


    


    chosen_file = view_file()
    # print(chosen_file)

    print("What do you want to do?")
    print("1. file overview")

    choice = input("enter a number")
    if choice  == 1:
        output_file_summary(chosen_file)




    # category - today - vs yesterday - vs last 7 days




    






if __name__ == "__main__":
    main_menu()







# categories:
#  Category                    | Which points to include                                                                                                |
# | --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
# | **NWELNG Send‑Outs**       | All **entry** flows at European LNG terminals in NW Europe—e.g. Zeebrugge, Gate (NL), Isle of Grain, Dunkirk.          |
# | **Russian Pipeline**        | All **exit** flows from Russia into Europe—e.g. Nord Stream 1 & 2 (DE), Yamal–Europe (PL→DE), Ukraine transit (UA→EU). |
# | **Norwegian Production**    | All **entry** flows from Norway—mostly through Emden (DE), Zeebrugge (BE), Dunkerque (FR).                             |
# | **UK Production**           | All **entry** flows from UK offshore—e.g. Bacton (IUK pipeline exit), St. Fergus, Teesside points.                     |
# | **North African Pipelines** | All **exit** flows from Algeria/Libya into Europe—Trans‑Med (DZ→IT), GME (LY→IT), Medgaz (DZ→ES).                      |
# | **TAP (Azerbaijan→EU)**     | The single **entry** point for Trans‑Adriatic Pipeline—often labelled “TAP” or “Greece–Italy interconnector.”          |


