def parse_gdp_data(data):
    """Parse GDP data from TradingEconomics API response."""
    return [[item["DateTime"], item["Value"]] for item in data if "DateTime" in item and "Value" in item]
