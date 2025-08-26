# app/routes.py
from app import flask_app
from flask import jsonify, request
from app.services.horoscope import calculate_chart

@flask_app.route('/')
def index():
    """
    A simple health check endpoint to confirm the server is running.
    """
    return jsonify({"status": "ok", "message": "MyGoddessUnknown API is running."})

@flask_app.route('/horoscope', methods=['POST'])
def calculate_horoscope():
    """
    API endpoint to calculate planetary positions.
    Expects a JSON payload with birth data.
    """
    # Get the JSON data from the request body
    data = request.get_json()

    required_fields = ['birth_date', 'birth_time', 'birth_timezone', 'latitude', 'longitude']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    # Call our updated service function
    result = calculate_chart(
        birth_date=data['birth_date'],
        birth_time=data['birth_time'],
        birth_timezone=data['birth_timezone'],
        latitude=float(data['latitude']),
        longitude=float(data['longitude'])
    )

    if result['status'] == 'error':
        return jsonify(result), 400
    
    return jsonify(result), 200
