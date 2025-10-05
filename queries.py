
from dotenv import load_dotenv
import re
from urllib.parse import quote
from flask import Flask, request, jsonify
import requests
import os
from google import genai
from google.genai import types
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)

# Set your Gemini and Search API keys in environment variables or here directly
os.environ["API_KEY"] = "GEMINI_API_KEY"
SEARCH_API_KEY = "API_KEY"  # This is for authenticating your /search calls if needed

# Initialize Gemini client once
client = genai.Client()



def sanitize_input(input_str):
    """Remove unwanted characters, keeping only alphanumeric and spaces."""
    return re.sub(r'[^a-zA-Z0-9s]', '', input_str)

def build_osdr_url(field, value):
    """Build an OSDR API query URL for a metadata search."""
    safe_value = quote(sanitize_input(value))
    base_url = "https://osdr.nasa.gov/osdr/data/search"
    query = f"?query=({field}={safe_value})&format=json"
    return base_url + query

def gemini_grounded_response(user_question, search_results):
    """
    Use Gemini to generate an improved response based on the search results.
    We send the user question plus relevant snippet data from your API search.
    """
    # Flatten snippets from your search results to provide context to Gemini
    snippets = """for hit in search_results.get("hits", {}).get("hits", []):
    study = hit.get("_source", {})
    title = study.get("Title", "")
    exp_platform = study.get("Experiment Platform", "")
    summary = study.get("Summary", "")
    snippets += f"Title: {title}
Platform: {exp_platform}
Summary: {summary}

"""

    prompt = (
    f'User question: {user_question}'
    f'Here are search results from the metadata API:{snippets}'
    'Summarize the most relevant findings from all the studies you can find, summarizing it and then providing a good explanation for all these studies for a general audience. start from the study protocol description part of the data you find. that is the result itself. only print your response. dont give the study articles '
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        print("Gemini API call failed:", str(e))
        return "Sorry, an error occurred while processing your request."

@app.route('/search', methods=['GET'])
def search_osdr():
    field = request.args.get('field')
    value = request.args.get('value')

    if not field or not value:
        return jsonify({"error": "Missing field or value"}), 400

    url = build_osdr_url(field, value)
    try:
        # Call your existing OSDR metadata search API
        response = requests.get(url)
        response.raise_for_status()
        search_json = response.json()

        # Use Gemini to generate an enhanced response based on the search results
        gemini_response = gemini_grounded_response(f"Search for {field} with value {value}", search_json)

        return jsonify({
            "Results": gemini_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)