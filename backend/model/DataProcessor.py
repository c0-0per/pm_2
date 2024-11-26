from model import Startup


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def detect_startups(self):
        keywords = ["funding", "investment", "Series A", "venture capital"]
        detected_startups = []

        for content in self.data.get("content", []):
            for keyword in keywords:
                if keyword.lower() in content.lower():
                    # dummy data
                    detected_startups.append(
                        Startup(
                            name="Example Startup",
                            founders=["John Doe", "Jane Smith"],
                            sector="Tech",
                            funding_round="Series A",
                            funding_amount=1000000,
                            tags=["AI", "Sustainability"],
                            country="Czech Republic"
                        )
                    )

                    break

        return detected_startups

    @staticmethod
    def apply_geo_filter(startups, countries):
        return [startup for startup in startups if startup.country in countries]

    @staticmethod
    def apply_impact_filter(startups, impacts):
        return [startup for startup in startups if any(tag in startup.tags for tag in impacts)]
