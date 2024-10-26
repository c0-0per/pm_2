from flask import Flask, request, jsonify
from model import Scraper as sc, DataSource as ds
import requests

app = Flask(__name__)
data_sources = []


@app.route("/data_source", methods=["POST"])
def add_data_source() -> tuple:
    data = request.json
    data_source = ds.DataSource(data["source_type"], data.get("url"), data.get("api_endpoint"))
    data_sources.append(data_source)
    return jsonify({"Message": "Data source added successfully!"}), 201


@app.route("/scrape", methods=["POST"])
def scrape_data() -> any:
    data = request.json
    source_index = data.get("source_index")

    if source_index < 0 or source_index >= len(data_sources):
        return jsonify({"Error": "Invalid data source index!"}), 400

    scraper = sc.Scraper(data_sources[source_index])
    scraped_data = scraper.scrape()
    return jsonify(scraped_data)


@app.route("/data_sources", methods=["GET"])
def get_data_sources() -> requests.Response:
    sources = [{
        "source_type": data_source.source_type,
        "url": data_source.url,
        "api_endpoint": data_source.api_endpoint
    } for data_source in data_sources]

    return jsonify(sources)


if __name__ == "__main__":
    app.run(debug=True)
