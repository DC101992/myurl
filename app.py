from flask import Flask, request, jsonify, redirect
import sqlite3

# Create Flask app
app = Flask(__name__)

# Initialize database if it doesn't exist
def init_db():
    conn = sqlite3.connect('shortener.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return "Welcome to MyURL Shortener!"

# Shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')

    if not long_url:
        return jsonify({'error': 'Long URL is required'}), 400

    short_code = generate_short_code(long_url)

    try:
        conn = sqlite3.connect('shortener.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Short code already exists'}), 400

    return jsonify({'short_url': f'https://{request.host}/{short_code}'})

# Redirect short URL
@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    conn = sqlite3.connect('shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return jsonify({'error': 'Short URL not found'}), 404

# Generate short code
def generate_short_code(long_url):
    return str(abs(hash(long_url)) % (10**6))  # Simple hash-based code

# Initialize database on startup
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
