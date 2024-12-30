import tradingeconomics as te

class BaseService:
    def __init__(self, api_base_url, api_base_key, http_client, allowed_countries):
        self.api_base_url = api_base_url
        self.api_base_key = api_base_key
        self.http_client = http_client
        self.allowed_countries = allowed_countries

    def validate_countries(self, country1, country2):
        """Validate whether the given countries are allowed."""
        return country1 in self.allowed_countries and country2 in self.allowed_countries

    def fetch_indicator_data(self, indicator, country):
        """Fetch data for a given indicator and country."""
        params = {"c": self.api_base_key}
        url = f"{self.api_base_url}/historical/country/{country}/indicator/{indicator}"
        response = self.http_client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def parse_time_series(self, data):
        """Extract date and value from the response."""
        return [(entry["DateTime"], entry["Value"]) for entry in data if entry.get("Value") is not None]
    
    def fetch_by_te(self,country, indicator, api_key, initDate):
        """Fetch GDP data using the Trading Economics library."""
        te.login(api_key)
        hist_data = te.getHistoricalData(country, indicator, initDate="2015-01-01")
        return hist_data
