# API Blueprint

from flask import Blueprint, jsonify, redirect, render_template, request
from config.settings import Config
from service.gdp_service import GDPService
from service.inflation_service import InflationService
from service.utility import http_client
from service.api_client import APIClient

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def index():
    return render_template("index.html")

@api_bp.route("/compare", methods=["GET"])
def compare_indicators():
    country1 = request.args.get("country1")
    country2 = request.args.get("country2")
    indicator = request.args.get("indicator")

    if not all([country1, country2, indicator]):
        return jsonify({"error": "Missing required query parameters"}), 400

    # Access allowed countries and API client from the Config
    allowed_countries = Config.ALLOWED_COUNTRIES
    api_client = APIClient(Config.API_BASE_URL,Config.API_KEY)
    
    gdp_service = GDPService(Config.API_BASE_URL, Config.API_KEY, http_client, allowed_countries)
    inflation_service = InflationService(Config.API_BASE_URL, Config.API_KEY, http_client, allowed_countries)


    if country1 not in allowed_countries or country2 not in allowed_countries:
        return jsonify({"error": "One or both countries are not allowed"}), 400

    try:
        if indicator.lower() == "gdp":
            service = gdp_service
        elif indicator.lower() == "inflation rate mom":
            service = inflation_service
        else:
            return jsonify({"error": f"Unsupported indicator: {indicator}"}), 400

        data1 = api_client.fetch_indicator_data(country1, indicator)
        data2 = api_client.fetch_indicator_data(country2, indicator)
        
        parsed_data1 = service.parse_time_series(data1)
        parsed_data2 = service.parse_time_series(data2)
        
        # Check for empty or invalid parsed data
        if not parsed_data1 or not parsed_data2:
            return jsonify({"error": f"No valid {indicator} data found for one or both countries: {country1}, {country2}."}), 404

        return jsonify({"country1_data": parsed_data1, "country2_data": parsed_data2})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
