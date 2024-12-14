from flask import Flask, jsonify, render_template, abort, send_file
import requests
import csv
import os
import datetime
import logging

# Flask application instance
app = Flask(__name__)

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

# Application constants
BASE_URL = 'https://rickandmortyapi.com/api/character/'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'characters.csv')

# Health check log
healthchecks = []

# Utility functions
def log_status(status, message, status_code):
    """Logs health check status and appends it to the healthchecks list."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        'Status': status,
        'Message': message,
        'Status code': status_code,
        'Timestamp': timestamp
    }
    healthchecks.append(entry)
    logging.info(f"{status} - {message} ({status_code})")

def save_results_to_csv(results):
    """Saves character data to a CSV file."""
    try:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Location', 'Image']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    except Exception as e:
        log_status("ERROR", f"Failed to save results to CSV: {e}", 500)
        abort(500)

def api_health_check():
    """Performs a health check for the external API."""
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            log_status("PASSED", "API healthcheck passed successfully.", 200)
        else:
            log_status("ERROR", f"API healthcheck failed. URL: {BASE_URL}", response.status_code)
            abort(500)
    except requests.RequestException as e:
        log_status("ERROR", f"API healthcheck request error: {e}", 500)
        abort(500)

def fetch_characters():
    """Fetches character data from the external API."""
    api_health_check()
    results = []
    url = BASE_URL
    params = {'species': 'Human', 'status': 'Alive'}

    try:
        while url:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            for character in data.get('results', []):
                if 'Earth' in character['location']['name']:
                    results.append({
                        'Name': character['name'],
                        'Location': character['location']['name'],
                        'Image': character['image']
                    })
            
            url = data.get('info', {}).get('next')
            params = None  # Clear params after the first request
    except requests.RequestException as e:
        log_status("ERROR", f"Error fetching characters: {e}", 500)
        abort(500)

    return results

# Routes
@app.route('/characters', methods=['GET'])
def display_characters():
    """Displays characters in an HTML template."""
    characters = fetch_characters()
    log_status("PASSED", "Characters page rendered successfully", 200)
    return render_template('characters.html', characters=characters)

@app.route('/download', methods=['GET'])
def download_characters():
    """Downloads character data as a CSV file."""
    characters = fetch_characters()
    save_results_to_csv(characters)
    return send_file(CSV_FILE, as_attachment=True, download_name='characters.csv')

@app.route('/healthcheck', methods=['GET'])
def health_check():
    """Returns the health check logs."""
    return jsonify({"status": "OK"}), 200

@app.route('/characters_data', methods=['GET'])
def characters_data():
    """Returns character data as JSON."""
    characters = fetch_characters()
    return jsonify(characters), 200

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html'), 200

@app.errorhandler(404)
def handle_not_found(error):
    """Handles 404 errors."""
    return render_template("404.html"), 404

@app.errorhandler(500)
def handle_internal_error(error):
    """Handles 500 errors."""
    return render_template('500.html'), 500

# Entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
