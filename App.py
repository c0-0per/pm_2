import requests
from flask import Flask, request, jsonify
from model import Scraper as sc, DataSource as ds

app = Flask(__name__)

# Airtable setup
AIRTABLE_API_KEY = 'patwN5zs8PvYco1aq.5186adce2a05f585419a30f20ed42c0ba9b0bf10aba6d8b19b8e46221890500e'
AIRTABLE_BASE_ID = 'appuToHM0Lp9zrj9C'
TABLE_NAME = 'Data Sources'

def add_data_source_to_airtable(data_source):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"fields": data_source}, headers=headers)
    return response.json()

def get_data_sources_from_airtable():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/data_source", methods=["POST"])
def add_data_source():
    data = request.json
    # Prepare data in Airtable-compatible format
    data_source = {
        "source_type": data["source_type"],
        "url": data.get("url"),
        "api_endpoint": data.get("api_endpoint")
    }
    airtable_response = add_data_source_to_airtable(data_source)
    return jsonify(airtable_response), 201

@app.route("/scrape", methods=["POST"])
def scrape_data():
    data = request.json
    source_index = data.get("source_index")
    airtable_data = get_data_sources_from_airtable()

    # Check if the source_index is valid
    if source_index < 0 or source_index >= len(airtable_data.get("records", [])):
        return jsonify({"Error": "Invalid data source index!"}), 400

    # Get the specific data source from Airtable records
    data_source_record = airtable_data["records"][source_index]["fields"]
    data_source = ds.DataSource(
        data_source_record["source_type"],
        data_source_record.get("url"),
        data_source_record.get("api_endpoint")
    )
    scraper = sc.Scraper(data_source)
    scraped_data = scraper.scrape()
    return jsonify(scraped_data)

@app.route("/data_sources", methods=["GET"])
def get_data_sources():
    airtable_data = get_data_sources_from_airtable()
    sources = [{
        "source_type": record["fields"].get("source_type"),
        "url": record["fields"].get("url"),
        "api_endpoint": record["fields"].get("api_endpoint")
    } for record in airtable_data.get("records", [])]

    return jsonify(sources)

if __name__ == "__main__":
    app.run(debug=True)
