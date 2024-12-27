import os
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.json.get("long_url")
    if not long_url:
        return jsonify({"error": "No URL provided"}), 400

    # Generate short URL logic here
    short_code = generate_short_code(long_url)

    # Store the mapping in the database
    save_url_mapping(long_url, short_code)

    short_url = f"https://myurl-ck9x.onrender.com/{short_code}"
    return jsonify({"short_url": short_url})

def generate_short_code(long_url):
    # Simple example of generating a short code (you can use any logic here)
    return hash(long_url) % 10000  # Just an example, for illustration purposes

def save_url_mapping(long_url, short_code):
    # Save the long_url and short_code in the database
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT, short_code TEXT)")
    cursor.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Use the PORT environment variable or default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
