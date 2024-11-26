import requests
import json
import time
import threading  # Imported for running Flask and automation concurrently
from flask import Flask, request, jsonify 
from model import Scraper as sc, DataSource as ds, DataProcessor as dp
#from pm2.frontend.add_to_airtable import add_data_to_airtable
import sys
import os
from add_to_airtable import add_data_to_airtable

other_folder_path = os.path.abspath('../frontend')

if other_folder_path not in sys.path:
    sys.path.append(other_folder_path)

from frontend import add_to_airtable

app = Flask(__name__)
data_sources = []
articles = []

# Airtable setup
AIRTABLE_API_KEY = 'patwN5zs8PvYco1aq.5186adce2a05f585419a30f20ed42c0ba9b0bf10aba6d8b19b8e46221890500e'
AIRTABLE_BASE_ID = 'appuToHM0Lp9zrj9C'
TABLE_NAME = 'Data Sources'

###kod Petra###

# Crunchbase setup
CRUNCHBASE_API_KEY = ""
CRUNCHBASE_BASE_URL = "https://api.crunchbase.com/v3.1"

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


def fetch_from_crunchbase(endpoint, params):
    url = f"{CRUNCHBASE_BASE_URL}/{endpoint}"
    headers = {
        "User-Agent": "",
        "Authorization": f"Bearer {CRUNCHBASE_API_KEY}"
    }
    params["user_key"] = CRUNCHBASE_API_KEY
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"Error": "Unable to fetch data from Crunchbase!"}


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


@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json
    scraped_data = data.get("scraped_data")
    countries = data.get("countries")
    impact = data.get("impact")

    if not scraped_data:
        return jsonify({"Error": "No scraped data provided!"}), 400

    processor = dp.DataProcessor(scraped_data)
    startups = processor.detect_startups()

    if countries:
        startups = processor.apply_geo_filter(startups, countries)

    if impact:
        startups = processor.apply_impact_filter(startups, impact)

    return jsonify([startup.to_dict() for startup in startups])


@app.route('/startups', methods=['GET'])
def get_crunchbase_startups():
    query = request.args.get("query", "")
    page = request.args.get("page", 1)
    params = {
        "query": query,
        "page": page
    }
    data = fetch_from_crunchbase("organizations", params)

    if "error" in data:
        return jsonify(data), 400

    startups = []

    for org in data.get("data"):
        org_properties = org.get("properties", {})
        startups.append({
            "LastUpdated": org_properties.get("updated_at"),
            "FoundedDate": org_properties.get("founded_on"),
            "Industry": org_properties.get("categories", []),
            "Founders": "Unknown",
            "FundingRound": "Unknown",
            "AmountRaised": org_properties.get("total_funding_usd", "Unknown"),
            "Tags": org_properties.get("short_description", "").split(),
            "Website": org_properties.get("homepage_url"),
            "Country": org_properties.get("location_country_code"),
            "Investors": "Unknown"
        })

    return jsonify(startups), 200


@app.route('/investors', methods=['GET'])
def get_crunchbase_investors():
    query = request.args.get("query", "")
    page = request.args.get("page", 1)
    params = {
        "query": query,
        "page": page
    }
    data = fetch_from_crunchbase("people", params)

    if "error" in data:
        return jsonify(data), 400

    investors = []

    for person in data.get("data"):
        person_properties = person.get("properties", {})
        investors.append({
            "investor_name": person_properties.get("first_name", "") + " " + person_properties.get("last_name", ""),
            "investor_type": "Unknown",
            "investment_amount": "Unknown",
            "contact_information": person_properties.get("email_address", "Unknown"),
            "associated_startups": [],
            "record_id": person.get("uuid")
        })

    return jsonify(investors), 200


@app.route('/funding_rounds', methods=['GET'])
def get_crunchbase_funding_rounds():
    query = request.args.get("query", "")
    page = request.args.get("page", 1)
    params = {
        "query": query,
        "page": page
    }
    data = fetch_from_crunchbase("funding_rounds", params)

    if "error" in data:
        return jsonify(data), 400

    funding_rounds = []

    for round_data in data.get("data"):
        round_properties = round_data.get("properties", {})
        funding_rounds.append({
            "round_type": round_properties.get("funding_type"),
            "amount_raised": round_properties.get("money_raised_usd", "Unknown"),
            "date": round_properties.get("announced_on"),
            "investors": round_properties.get("investor_names", "Unknown")
        })

    return jsonify(funding_rounds), 200


@app.route('/')
def home():
    return "Hello, Render and Airtable!"


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
        with open("../output/scraped_data.json", "w") as f: 
            json.dump(scraped_data, f, indent=4)
    except requests.exceptions.RequestException as e:
        with open("../output/scraped_data.json", "w") as f:
            json.dump({"Error": str(e)}, f, indent=4)

def background_task():
    while True:
        print("Running Airtable update...")
        add_data_to_airtable()
        time.sleep(3600)  # Run every hour


if __name__ == "__main__":
    threading.Thread(target=background_task, daemon=True).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    # flask_thread = threading.Thread(target=run_flask)  # create thread to run Flask
    # flask_thread.daemon = True  # so that the thread exits when the main program does
    # flask_thread.start()  # first start the flask thread
    
    # automate_commands()  # then the commands thread
    # add_to_airtable.add_data_to_airtable()
