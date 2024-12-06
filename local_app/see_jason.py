import requests
import json

# Base URL for the Rick and Morty API
BASE_URL = 'https://rickandmortyapi.com/api/character'

# Parameters for filtering characters
params = {
    'species': 'Human',
    'status': 'Alive',
}

# Make the API request
response = requests.get(BASE_URL, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Get the JSON data

    # Save JSON data to a file
    with open('rick_and_morty_data.json', 'w') as file:
        json.dump(data, file, indent=4)  # Pretty-print JSON with indentation

    print("JSON data has been saved to 'rick_and_morty_data.json'")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
