from flask import Flask, redirect, request, abort
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for short URL redirection
@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = get_db_connection()
    url_mapping = conn.execute(
        'SELECT long_url FROM url_mappings WHERE short_code = ?',
        (short_code,)
    ).fetchone()
    conn.close()
    
    if url_mapping:
        return redirect(url_mapping['long_url'], code=302)
    else:
        abort(404, description="Short URL not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
