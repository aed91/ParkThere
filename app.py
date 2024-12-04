from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os
import csv

# Initialize Flask app and enable CORS
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Path to CSV file containing parking data
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), 'api_data_export.csv')

# API Endpoint to fetch parking data
@app.route('/get-data', methods=['GET'])
def get_data():
    data = []

    try:
        # Open the CSV file
        with open(CSV_FILE_PATH, mode='r') as file:
            csv_reader = csv.DictReader(file)  # Use DictReader for column-based access

            # Read all rows from the CSV and transform into expected format
            for row in csv_reader:
                try:
                    # Extract relevant columns and ensure correct data types
                    spot = {
                        "id": int(row["id"]),
                        "total_spots": int(row["total_spots"]),
                        "free_spots": int(row["free_spots"]),
                        "occupied_spots": int(row["occupied_spots"]),
                        "last_updated": row["last_updated"]
                    }
                    data.append(spot)
                except ValueError as e:
                    print(f"Skipping invalid row: {row} ({e})")
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {e}"}), 500

    if not data:
        return jsonify({"message": "No data available in CSV"}), 404

    return jsonify({"csv_data": data}), 200


# Endpoint for /parking-data (if necessary)
@app.route('/parking-data', methods=['GET'])
def get_parking_data():
    data = []
    try:
        with open(CSV_FILE_PATH, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                spot = {
                    "id": int(row["id"]),
                    "total_spots": int(row["total_spots"]),
                    "free_spots": int(row["free_spots"]),
                    "occupied_spots": int(row["occupied_spots"]),
                    "last_updated": row["last_updated"]
                }
                data.append(spot)
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {e}"}), 500

    if not data:
        return jsonify({"message": "No data available in CSV"}), 404

    return jsonify({"csv_data": data}), 200


# Route for the About page
@app.route('/about')
def about():
    return render_template('pages/about.html')  # Ensure it's in the /templates/pages folder

# Route for the Contact page
@app.route('/contact')
def contact():
    return render_template('pages/contact.html')  # Ensure it's in the /templates/pages folder

# Route for the Display page
@app.route('/display')
def display():
    return render_template('pages/display.html')  # Ensure it's in the /templates/pages folder


@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    # Simple health check endpoint
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

