from bs4 import BeautifulSoup
from model import DataSource
import feedparser
import requests

from datetime import datetime


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

    def fetch_newsapi_data(self):
        try:
            response = requests.get(self.data_source.api_endpoint[0], self.data_source.api_endpoint[1])
            response.raise_for_status()
            articles = response.json().get("articles", [])
            formatted_articles = []

            for article in articles:
                article_data = {
                    "Source Name": article.get("source", {}).get("name"),
                    "Source URL": article.get("url"),
                    "Data Type": ["Startups"],
                    "Collection Frequency": "Daily",
                    "Last Updated": datetime.now().strftime("%Y-%m-%d"),
                    "Associated Countries": [],
                    "Related Tracking Reports": [],
                    "Startups": []
                }

                formatted_articles.append(article_data)

            return formatted_articles
        except Exception as e:
            return {"Error": str(e)}
