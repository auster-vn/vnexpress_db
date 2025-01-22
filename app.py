from flask import Flask, request, jsonify, render_template
import subprocess
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_summary_data', methods=['GET'])
def get_summary_data():
    rows = []
    try:
        with open('vnexpress_summarized.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        pass  # Handle file not found case
    return jsonify(rows)

@app.route('/run_crawl', methods=['POST'])
def run_crawl():
    try:
        subprocess.run(['python3', 'crawl.py'], check=True)
        return jsonify({'message': 'Crawl completed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error running crawl.', 'error': str(e)}), 500

@app.route('/run_content', methods=['POST'])
def run_content():
    try:
        subprocess.run(['python3', 'content.py'], check=True)
        return jsonify({'message': 'Content extraction completed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error running content extraction.', 'error': str(e)}), 500

@app.route('/run_summary', methods=['POST'])
def run_summary():
    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'message': 'API Key is required.'}), 400

    try:
        with open('api_key.txt', 'w') as f:
            f.write(api_key)
        subprocess.run(['python3', 'summary.py'], check=True)
        return jsonify({'message': 'Summary generation completed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error running summary.', 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

