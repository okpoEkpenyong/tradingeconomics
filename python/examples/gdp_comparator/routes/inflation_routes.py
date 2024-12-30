from flask import Blueprint, jsonify, request

inflation_routes = Blueprint('inflation_routes', __name__)

@inflation_routes.route('/api/inflation', methods=['GET'])
def get_inflation_data():
    # Fetch inflation data logic here
    return jsonify({"message": "Inflation data"})
