class Startup:
    def __init__(self, name, founders, sector, funding_round, funding_amount, tags, country):
        self.name = name
        self.founders = founders
        self.sector = sector
        self.funding_round = funding_round
        self.funding_amount = funding_amount
        self.tags = tags
        self.country = country

    def to_dict(self):
        return {
            "name": self.name,
            "founders": self.founders,
            "sector": self.sector,
            "funding_round": self.funding_round,
            "funding_amount": self.funding_amount,
            "tags": self.tags,
            "country": self.country
        }
