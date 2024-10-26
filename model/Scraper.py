from bs4 import BeautifulSoup
from model import DataSource
import feedparser
import requests


class Scraper:
    def __init__(self, data_source: DataSource) -> None:
        self.data_source = data_source

    def scrape(self) -> dict:
        if self.data_source.source_type.lower() == "website":
            return self.scrape_website()
        elif self.data_source.source_type.lower() == "rss":
            return self.fetch_rss_data()
        elif self.data_source.source_type.lower() == "newsapi":
            return self.fetch_newsapi_data()
        else:
            return {"Error": "Unsupported data source type!"}

    def scrape_website(self) -> dict:
        try:
            response = requests.get(self.data_source.url[0])
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = [paragraph.text for paragraph in soup.find_all(self.data_source.url[1])]
            return {"Content": paragraphs}
        except Exception as e:
            return {"Error": str(e)}

    def fetch_rss_data(self) -> dict:
        try:
            feed = feedparser.parse(self.data_source.url[0])
            articles = []

            for entry in feed.entries:
                if self.data_source.url[1] == [] or any(keyword.lower() in entry.title.lower() or
                                                        keyword.lower() in entry.summary.lower()
                                                        for keyword in self.data_source.url[1]):
                    articles.append({"title": entry.title, "link": entry.link, "summary": entry.summary})
            return {"Articles": articles}
        except Exception as e:
            return {"Error": str(e)}

    def fetch_newsapi_data(self) -> dict:
        try:
            response = requests.get(self.data_source.api_endpoint[0], self.data_source.api_endpoint[1])
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}
