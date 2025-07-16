import requests, pathlib
from datetime import datetime, timedelta, date
import os
import requests
import pathlib
import csv
from tabulate import tabulate


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

    dest = pathlib.Path(f"operationalData_{to_date}.csv")

    try:
        r = requests.get(base, params=params, timeout=60)
        r.raise_for_status()              # will raise if HTTP 4xx/5xx
        dest.write_bytes(r.content)       # plain‑text CSV
        print(f"Saved to {dest.resolve()}")
    except Exception as e:
        print("error :(")



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


    with open(chosen_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
            
        # Fields to display
        fields_to_show = ['periodFrom', 'periodType', 'pointLabel', 'directionKey', 'indicator', 'value', 'unit']

        table_data = []
        for row in reader:
            # Extract required fields
            filtered_row = [row.get(field, 'N/A') for field in fields_to_show]
            table_data.append(filtered_row)
        
        # Create headers
        headers = ['Period From', 'Period Type', 'Point Label', 'Direction Key', 'Indicator', 'Value', 'Unit']
        
        # Display table
        print(f"\n{'-'*80}")
        print("GAS FLOW DATA TABLE")
        print(f"{'-'*80}")
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        print(f"\nTotal records: {len(table_data)}")
        

    



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
            chosen_file = view_file()
            print(chosen_file)







        


        # viewing

        # default view : indicator, pointlabel, tsoidentifier

        # custom view




if __name__ == "__main__":
    main_menu()




