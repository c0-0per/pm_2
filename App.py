from flask import Flask, request, jsonify
from model import Scraper as sc, DataSource as ds
import requests

app = Flask(__name__)
data_sources = []

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


@app.route("/add_data_source", methods=["POST"])
def add_data_source() -> tuple:
    data = request.json
    data_source = ds.DataSource(data["source_type"], data.get("url"), data.get("api_endpoint"))
    data_sources.append(data_source)
    return jsonify({"Message": "Data source added successfully!"}), 201


@app.route("/scrape_data", methods=["POST"])
def scrape_data() -> any:
    data = request.json
    source_index = data.get("source_index")

    if source_index < 0 or source_index >= len(data_sources):
        return jsonify({"Error": "Invalid data source index!"}), 400

    scraper = sc.Scraper(data_sources[source_index])
    scraped_data = scraper.scrape()
    return jsonify(scraped_data)


@app.route("/get_data_sources", methods=["GET"])
def get_data_sources() -> requests.Response:
    sources = [{
        "source_type": data_source.source_type,
        "url": data_source.url,
        "api_endpoint": data_source.api_endpoint
    } for data_source in data_sources]

    return jsonify(sources)


@app.route("/save_data_source", methods=["POST"])
def save_data_source():
    data_source = request.json
    airtable_response = add_data_source_to_airtable(data_source)
    return jsonify(airtable_response), 201


@app.route("/load_data_sources", methods=["GET"])
def load_data_sources():
    airtable_data = get_data_sources_from_airtable()
    sources = [record for record in airtable_data.get("records", [])]
    return jsonify(sources)


if __name__ == "__main__":
    app.run(debug=True)
