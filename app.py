from flask import Flask, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# API Endpoint to fetch parking data
@app.route('/get-data', methods=['GET'])
def get_data():
    data = []
    csv_file_path = os.path.join(os.path.dirname(__file__), 'sample_parking_data.csv')

    try:
        # Open the CSV file
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            # Read all rows from the CSV
            for row in csv_reader:
                data.append(row)  # Append each row as a list
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {e}"}), 500

    if not data:
        return jsonify({"message": "No data available in CSV"}), 404

    return jsonify({"csv_data": data}), 200

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == '__main__':
    # Replace 0.0.0.0 with your server's IP or keep as is for global access
    app.run(host='0.0.0.0', port=5000)
