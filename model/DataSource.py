class DataSource:
    def __init__(self, source_type: str, url: list, api_endpoint: list) -> None:
        self.source_type = source_type
        self.url = url
        self.api_endpoint = api_endpoint
