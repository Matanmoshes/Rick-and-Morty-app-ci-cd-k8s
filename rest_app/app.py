from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Base URL for the Rick and Morty API
BASE_URL = 'https://rickandmortyapi.com/api/character'
params = {
    'species': 'Human',
    'status': 'Alive',
}

# Fetch data at startup
def fetch_characters():
    characters = []
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Paginate through all results
    while True:
        for character in data['results']:
            # Check if origin contains "Earth"
            if 'Earth' in character['origin']['name']:
                name = character['name']
                location = character['location']['name']
                image = character['image']
                characters.append({
                    'Name': name,
                    'Location': location,
                    'Image': image
                })

        next_page = data['info']['next']
        if next_page:
            response = requests.get(next_page)
            data = response.json()
        else:
            break

    return characters

# Store fetched data in a global variable
CHARACTERS_DATA = fetch_characters()

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "OK"}), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    return jsonify(CHARACTERS_DATA), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
