from flask import Flask, request, jsonify
import re
import requests
from urllib.parse import quote
from flask_cors import CORS  # to allow frontend JS requests

app = Flask(__name__)
CORS(app)

def sanitize_input(input_str):
    """Remove unwanted characters, keeping only alphanumeric and spaces."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', input_str)

def build_osdr_url(field, value):
    """Build an OSDR API query URL for a metadata search."""
    safe_value = quote(sanitize_input(value))
    base_url = "https://osdr.nasa.gov/osdr/data/search"
    query = f"?query=({field}={safe_value})&format=json"
    return base_url + query

@app.route('/search', methods=['GET'])
def search_osdr():
    field = request.args.get('field')
    value = request.args.get('value')

    if not field or not value:
        return jsonify({"error": "Missing field or value"}), 400

    url = build_osdr_url(field, value)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)