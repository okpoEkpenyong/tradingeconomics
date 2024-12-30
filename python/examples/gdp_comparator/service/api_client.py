import requests

class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def _make_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        params = params or {}
        params["c"] = self.api_key
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_indicator_data(self, country, indicator):
        endpoint = f"historical/country/{country}/indicator/{indicator}"
        return self._make_request(endpoint)

    def fetch_inflation_data(self, country):
        endpoint = f"historical/country/{country}/indicator/inflation"
        return self._make_request(endpoint)
