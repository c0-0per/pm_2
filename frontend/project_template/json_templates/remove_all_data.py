import requests
import json
import time

AIRTABLE_API_KEY = 'patwN5zs8PvYco1aq.5186adce2a05f585419a30f20ed42c0ba9b0bf10aba6d8b19b8e46221890500e' 
AIRTABLE_BASE_ID = 'appuToHM0Lp9zrj9C' 


TABLE_NAMES = ['Data Sources', 'Tracking Reports', 'Investors', 'Countries', 'Startups']

def get_all_records(table_name):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}" 
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}" 
    }
    records = []
    params = {
        "pageSize": 100 
    }
    while True:
        response = requests.get(url, headers=headers, params=params) 
        if response.status_code != 200:
            print(f"Error fetching records from '{table_name}': {response.text}") 
            break
        data = response.json()
        records.extend(data.get('records', [])) 
        if 'offset' in data:
            params['offset'] = data['offset']  
        else:
            break 
    return records

def delete_record(table_name, record_id):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}/{record_id}"  
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}" 
    }
    response = requests.delete(url, headers=headers)  
    if response.status_code == 200:
        print(f"Successfully deleted record {record_id} from '{table_name}'.")  
    else:
        print(f"Failed to delete record {record_id} from '{table_name}': {response.text}")  

def delete_all_records(table_names):
    for table_name in table_names:
        print(f"\nProcessing table: '{table_name}'")
        records = get_all_records(table_name) 
        print(f"Found {len(records)} records to delete in '{table_name}'.")
        for record in records:
            record_id = record['id']  
            delete_record(table_name, record_id) 
            time.sleep(0.2) 
        print(f"Completed deletion for table: '{table_name}'")

if __name__ == "__main__":
    delete_all_records(TABLE_NAMES)  
