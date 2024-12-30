from flask import Blueprint, jsonify, request
from service.api_client import APIClient
from config.settings import Config
from service.utility.http_client import RequestsHTTPClient
from routes import gdp_routes

http_client = RequestsHTTPClient()

@gdp_routes.route('/api/gdp', methods=['GET'])
def get_gdp_data(indicator, country):
    client = APIClient(Config.API_BASE_URL, Config.API_KEY, http_client)
    params = {"c": Config.API_KEY}
    url = f"{Config.API_BASE_URL}/historical/country/{country}/indicator/{indicator}"
    gdp_data = client.fetch_data("gdp_endpoint")
    return jsonify(gdp_data)
