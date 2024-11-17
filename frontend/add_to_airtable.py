import requests
import json

# Airtable setup
AIRTABLE_API_KEY = 'patwN5zs8PvYco1aq.5186adce2a05f585419a30f20ed42c0ba9b0bf10aba6d8b19b8e46221890500e'
AIRTABLE_BASE_ID = 'appuToHM0Lp9zrj9C'
TABLE_NAME = 'Data Sources'

def add_row_to_airtable(row, table_name):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}" 
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"fields": row}, headers=headers)  
    return response.json()

def add_scraped_data_to_airtable(scraped_data, table_name):
    for entry in scraped_data:
        row = {
            "Associated Countries": entry.get("Associated Countries", []),
            "Collection Frequency": entry.get("Collection Frequency", ""),
            "Data Type": entry.get("Data Type", []),
            "Last Updated": entry.get("Last Updated", ""),
            "Related Tracking Reports": entry.get("Related Tracking Reports", []),
            "Source Name": entry.get("Source Name", ""),
            "Source URL": entry.get("Source URL", ""),
            "Startups": entry.get("Startups", [])
        }
    
        airtable_response = add_row_to_airtable(row, table_name)
        
        if 'error' in airtable_response:
            print(f"Error adding {row['Source Name']} to Airtable: {airtable_response['error']}")
        else:
            record_id = airtable_response.get('id')
            print(f"Successfully added {row['Source Name']} to Airtable with record_id {record_id}.")

def add_data_to_airtable():
    try:
        with open('../output/scraped_data.json', 'r', encoding='utf-8') as f:
            scraped_data = json.load(f)
    except FileNotFoundError:
        print("../output/scraped_data.json file not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Add the scraped data to Airtable
    add_scraped_data_to_airtable(scraped_data, TABLE_NAME)

if __name__ == "__main__":
    add_data_to_airtable()
