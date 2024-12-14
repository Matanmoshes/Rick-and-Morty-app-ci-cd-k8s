from flask import Flask, jsonify, render_template, abort, send_file
import requests
import csv
import os
import datetime
import logging

app = Flask(__name__)

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

# Constants for external resources and file paths
CHAR_API_BASE = 'https://rickandmortyapi.com/api/character/'
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
CHAR_CSV = os.path.join(WORKING_DIR, 'characters.csv')

# Health checks log buffer
health_records = []

def record_status(state, detail, code):
    """Record application health or error status."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        'State': state,
        'Detail': detail,
        'Code': code,
        'Time': now
    }
    health_records.append(log_entry)
    logging.info(f"{state} - {detail} ({code})")

def write_csv(character_data):
    """Write character info to a CSV file."""
    try:
        with open(CHAR_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            headers = ['Name', 'Location', 'Image']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(character_data)
    except Exception as err:
        record_status("ERROR", f"Unable to save CSV: {err}", 500)
        abort(500)

def check_api_health():
    """Check availability of the external Rick and Morty API."""
    try:
        resp = requests.get(CHAR_API_BASE, timeout=5)
        if resp.status_code == 200:
            record_status("OK", "External API is responsive.", 200)
        else:
            record_status("ERROR", f"External API issue at {CHAR_API_BASE}", resp.status_code)
            abort(500)
    except requests.RequestException as err:
        record_status("ERROR", f"API request error: {err}", 500)
        abort(500)

def retrieve_characters():
    """Retrieve all human, alive characters originating from an Earth variant."""
    check_api_health()
    outcome = []
    next_url = CHAR_API_BASE
    query_params = {'species': 'Human', 'status': 'Alive'}

    try:
        while next_url:
            r = requests.get(next_url, params=query_params, timeout=10)
            r.raise_for_status()
            info = r.json()

            for char in info.get('results', []):
                if 'Earth' in char['location']['name']:
                    outcome.append({
                        'Name': char['name'],
                        'Location': char['location']['name'],
                        'Image': char['image']
                    })
            
            next_url = info.get('info', {}).get('next')
            query_params = None
    except requests.RequestException as err:
        record_status("ERROR", f"Character retrieval failed: {err}", 500)
        abort(500)

    return outcome

@app.route('/characters', methods=['GET'])
def show_characters():
    """Render a page displaying character data."""
    chars = retrieve_characters()
    record_status("OK", "/characters rendered successfully", 200)
    return render_template('characters.html', characters=chars)

@app.route('/download', methods=['GET'])
def download_csv():
    """Download the character data in CSV format."""
    chars = retrieve_characters()
    write_csv(chars)
    return send_file(CHAR_CSV, as_attachment=True, download_name='characters.csv')

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Respond with overall health status of the service."""
    return jsonify({"status": "OK"}), 200

@app.route('/characters_data', methods=['GET'])
def chars_json():
    """Return character data as JSON."""
    chars = retrieve_characters()
    return jsonify(chars), 200

@app.route('/')
def root():
    """Render the main index page."""
    return render_template('index.html'), 200

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors by showing a custom page."""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle unexpected server errors with a custom page."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
