# Rick and Morty Local App

## Overview
The **Rick and Morty Local App** is a simple script designed for development and testing purposes. 
The goal of this script is to:
1. Query the **Rick and Morty API** to find all characters that meet the following conditions:
   - **Species**: Human
   - **Status**: Alive
   - **Origin**: Earth
2. Generate a list of results including:
   - Name
   - Location
   - Image link
3. Write the results to a CSV file in the following format:
   ```csv
   Name,Location,Image
   Rick Sanchez,Earth (C-137),https://rickandmortyapi.com/api/character/avatar/1.jpeg
   ```

For more details about the API, refer to the [Rick and Morty API documentation](https://rickandmortyapi.com/documentation/#rest).

---

## Script Details
The script is written in Python and performs the following steps:
1. **Fetch Data**: Makes an API request to fetch characters matching the conditions for species and status.
2. **Filter Data**: Loops through all API pages and filters characters whose origin includes "Earth."
3. **Store Data**: Collects the filtered data (name, location, and image) and writes it to a CSV file.

---

## Prerequisites
- Python 3.x installed on your local machine.
- `requests` library installed:
  ```bash
  pip install requests
  ```

---

## How to Run the Script
1. Clone the repository or copy the script to your local machine.
```bash
git clone https://github.com/Matanmoshes/Rick-and-Morty-app-ci-cd-k8s.git
```
2. Navigate to the folder containing the script.
```bash
cd Rick-and-Morty-app-ci-cd-k8s
```
3. Run the script:
```bash
python app.py
```
4. After running, the script will create a file named `characters.csv` in the same directory, containing the filtered data.

---

## Example Output
The generated `characters.csv` file will look like this:
```csv
Name,Location,Image
Rick Sanchez,Earth (C-137),https://rickandmortyapi.com/api/character/avatar/1.jpeg
Morty Smith,Earth (C-137),https://rickandmortyapi.com/api/character/avatar/2.jpeg
Summer Smith,Earth (Replacement Dimension),https://rickandmortyapi.com/api/character/avatar/3.jpeg
```
**Here is link to the file created [characters.csv](https://github.com/Matanmoshes/Rick-and-Morty-app-ci-cd-k8s/blob/main/local_app/characters.csv)**
---

## Refference Links
- [Rick and Morty API Documentation](https://rickandmortyapi.com/documentation/#rest)
- [Project Root Directory](https://github.com/Matanmoshes/Rick-and-Morty-app-ci-cd-k8s)
