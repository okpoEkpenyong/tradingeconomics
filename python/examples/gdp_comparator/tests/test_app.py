import pytest
from python.examples.gdp_comparator.main import app
import responses
from flask import jsonify

@pytest.fixture
def client():
    """Fixture for setting up a Flask test client."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def runner():
    """Fixture for setting up a Flask CLI runner."""
    return app.test_cli_runner()

# Mock API Base URL
API_BASE_URL = "https://api.tradingeconomics.com"

def mock_api_response(url, status=200, json_data=None):
    """Helper function to mock external API responses."""
    responses.add(
        responses.GET,
        url,
        json=json_data or {},
        status=status,
        content_type="application/json"
    )

# Test cases
def test_index_page(client):
    """Test that the index page loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"TradingEconomics Comparator" in response.data

@responses.activate
def test_compare_api_success(client):
    """Test the API endpoint for valid input."""
    mexico_url = f"{API_BASE_URL}/historical/country/Mexico/indicator/GDP"
    sweden_url = f"{API_BASE_URL}/historical/country/Sweden/indicator/GDP"

    mock_api_response(mexico_url, json_data=[
        {"DateTime": "2023-01-01T00:00:00", "Value": 123.45}
    ])
    mock_api_response(sweden_url, json_data=[
        {"DateTime": "2023-01-01T00:00:00", "Value": 678.90}
    ])

    response = client.get("/api/data?country1=Mexico&country2=Sweden")
    assert response.status_code == 200
    data = response.get_json()
    assert "mexico_gdp" in data
    assert "sweden_gdp" in data
    assert len(data["mexico_gdp"]) == 1
    assert len(data["sweden_gdp"]) == 1

@responses.activate
def test_compare_api_invalid_country(client):
    """Test the API endpoint with an invalid country."""
    invalid_url = f"{API_BASE_URL}/historical/country/InvalidCountry/indicator/GDP"
    mock_api_response(invalid_url, status=404)

    response = client.get("/api/data?country1=InvalidCountry&country2=Sweden")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert "Data not found" in data["error"]

@responses.activate
def test_compare_api_malformed_input(client):
    """Test the API endpoint with malformed input."""
    response = client.get("/api/data?country1=Mexico123&country2=Sweden!@#")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Invalid country names provided" in data["error"]

@responses.activate
def test_compare_api_network_error(client):
    """Test the API endpoint with a network error."""
    mexico_url = f"{API_BASE_URL}/historical/country/Mexico/indicator/GDP"
    responses.add(
        responses.GET,
        mexico_url,
        body=Exception("Network error"),
        status=500,
    )

    response = client.get("/api/data?country1=Mexico&country2=Sweden")
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert "An unexpected error occurred" in data["error"]

@responses.activate
def test_compare_api_empty_response(client):
    """Test the API endpoint when the API returns an empty response."""
    mexico_url = f"{API_BASE_URL}/historical/country/Mexico/indicator/GDP"
    sweden_url = f"{API_BASE_URL}/historical/country/Sweden/indicator/GDP"

    mock_api_response(mexico_url, json_data=[])
    mock_api_response(sweden_url, json_data=[])

    response = client.get("/api/data?country1=Mexico&country2=Sweden")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert "No valid GDP data found" in data["error"]

@responses.activate
def test_compare_api_partial_success(client):
    """Test the API endpoint when one country's data is missing."""
    mexico_url = f"{API_BASE_URL}/historical/country/Mexico/indicator/GDP"
    sweden_url = f"{API_BASE_URL}/historical/country/Sweden/indicator/GDP"

    mock_api_response(mexico_url, json_data=[
        {"DateTime": "2023-01-01T00:00:00", "Value": 123.45}
    ])
    mock_api_response(sweden_url, status=404)

    response = client.get("/api/data?country1=Mexico&country2=Sweden")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert "Data not found for one or both countries" in data["error"]
