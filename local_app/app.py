import requests
import csv

# Base URL for the Rick and Morty API
BASE_URL = 'https://rickandmortyapi.com/api/character'

# Parameters for filtering characters
params = {
    'species': 'Human',
    'status': 'Alive',
    # We will manually filter for Earth origins.
}

# List to store characters that meet all conditions
characters = []

# Initial API request
response = requests.get(BASE_URL, params=params)
data = response.json()

# Loop through all pages
while True:
    for character in data['results']:
        # Check if the character's origin includes "Earth"
        # This will capture "Earth (C-137)", "Earth (Replacement Dimension)", etc.
        if 'Earth' in character['origin']['name']:
            # Collect the required information
            name = character['name']
            location = character['location']['name']
            image = character['image']
            characters.append({'Name': name, 'Location': location, 'Image': image})
    # Check if there is a next page
    if data['info']['next']:
        response = requests.get(data['info']['next'])
        data = response.json()
    else:
        break

# Write the results to a CSV file
with open('characters.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Location', 'Image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for character in characters:
        writer.writerow(character)

print("CSV file 'characters.csv' has been created with the filtered character data.")
