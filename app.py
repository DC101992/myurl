from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Define the path to the SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'urls.db')

# Ensure the database and table are created if they do not exist
def init_db():
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_url TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

# Route to shorten URLs
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    # Check if the 'long_url' key exists in the request
    if 'long_url' not in data:
        return jsonify({"error": "No URL provided"}), 400

    long_url = data['long_url']
    short_url = generate_short_code(long_url)

    # Save the URL and its shortened code into the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
    conn.commit()
    conn.close()

    return jsonify({"long_url": long_url, "short_url": short_url})

# Function to generate a short code from the long URL
def generate_short_code(long_url):
    # A simple function to generate a short code. Modify it as needed.
    return long_url[-6:]  # Example: using the last 6 characters of the URL (you can enhance this)

# Initialize the database when the app starts
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

