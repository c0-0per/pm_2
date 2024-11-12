import requests
import json
import time
import threading  # Imported for running Flask and automation concurrently
from flask import Flask, request, jsonify 
from model import Scraper as sc, DataSource as ds
from add_to_airtable import add_data_to_airtable

app = Flask(__name__)
data_sources = []
articles = []

# Airtable setup
AIRTABLE_API_KEY = 'patwN5zs8PvYco1aq.5186adce2a05f585419a30f20ed42c0ba9b0bf10aba6d8b19b8e46221890500e'
AIRTABLE_BASE_ID = 'appuToHM0Lp9zrj9C'
TABLE_NAME = 'Data Sources'

###kod Petra###

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
    articles.extend(scraped_data)
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
    data = request.json
    source_index = data.get("source_index")
    airtable_response = add_data_source_to_airtable(articles[source_index])
    return jsonify(airtable_response), 201


@app.route("/load_data_sources", methods=["GET"])
def load_data_sources():
    airtable_data = get_data_sources_from_airtable()
    sources = [record for record in airtable_data.get("records", [])]
    return jsonify(sources)


#new code
def run_flask():
    app.run(debug=True, use_reloader=False) 

#new code
def automate_commands():
    time.sleep(2)  # wait for the flask app to start
    add_commands = [  # commands to save data sources
        {
            "url": "http://127.0.0.1:5000/add_data_source",
            "method": "POST",
            "json": {
                "source_type": "website",
                "url": [
                    "https://www.example.com",
                    "p"
                ]
            }
        },
        {
            "url": "http://127.0.0.1:5000/add_data_source",
            "method": "POST",
            "json": {
                "source_type": "rss",
                "url": [
                    "https://www.czechcrunch.cz/feed",
                    ["funding", "fundraising", "Series A", "venture capital", "investment"]
                ]
            }
        },
        {
            "url": "http://127.0.0.1:5000/add_data_source",
            "method": "POST",
            "json": {
                "source_type": "newsapi",
                "api_endpoint": [
                    "https://newsapi.org/v2/everything",
                    {
                        "q": "funding fundraising 'Series A' 'venture capital' investment",
                        "language": "en",
                        "pageSize": 5,
                        "apiKey": "2c712beed2a24fea95394aa9a3b56655"
                    }
                ]
            }
        }
    ]
    
    add_outputs = []
    
    # execute the commands
    for command in add_commands:
        if command["method"] == "POST":
            try:
                response = requests.post(command["url"], json=command["json"])
                add_outputs.append(response.json())
            except requests.exceptions.RequestException as e:
                add_outputs.append({"Error": str(e)})

    
    # scrape command from one of the data sources (currently newsapi)
    scrape_command = {
        "url": "http://127.0.0.1:5000/scrape_data",
        "method": "POST",
        "json": {
            "source_index": 2 
        }
    }
    
    #running the scrape command
    try:
        response = requests.post(scrape_command["url"], json=scrape_command["json"])
        scraped_data = response.json()
        with open("scraped_data.json", "w") as f: 
            json.dump(scraped_data, f, indent=4)
    except requests.exceptions.RequestException as e:
        with open("scraped_data.json", "w") as f:
            json.dump({"Error": str(e)}, f, indent=4)


if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)  # create thread to run Flask
    flask_thread.daemon = True  # so that the thread exits when the main program does
    flask_thread.start()  # first start the flask thread
    
    automate_commands()  # then the commands thread
    add_data_to_airtable()
