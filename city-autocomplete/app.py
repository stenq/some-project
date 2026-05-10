from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify([])

    url = "https://api.geoapify.com/v1/geocode/autocomplete"
    
    params = {
        'text': query,
        'type': 'city',           # ищем только города
        'limit': 10,
        'apiKey': GEOAPIFY_API_KEY
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return jsonify([])

    data = response.json()
    suggestions = []

    for feature in data.get('features', []):
        props = feature.get('properties', {})
        city = props.get('city') or props.get('name')
        country = props.get('country')
        
        if city:
            label = f"{city}, {country}" if country else city
            suggestions.append({
                'label': label,
                'city': city,
                'country': country
            })

    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)