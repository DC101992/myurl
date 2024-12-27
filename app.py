from flask import Flask, request, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

# Function to create a random short code (You can improve this logic if needed)
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    try:
        # Step 1: Parse the incoming JSON data
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400

        long_url = data['url']

        # Step 2: Connect to the SQLite database and check if it exists (you need to handle this part in the database)
        conn = sqlite3.connect('urls.db')  # Ensure this is in the same directory or provide the full path
        cursor = conn.cursor()

        # Step 3: Check if the long URL is already in the database
        cursor.execute("SELECT short_code FROM urls WHERE long_url = ?", (long_url,))
        row = cursor.fetchone()

        if row:
            # If the URL already has a short code, return it
            short_code = row[0]
        else:
            # Generate a new short code
            short_code = generate_short_code()

            # Step 4: Insert the new long URL and short code into the database
            cursor.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
            conn.commit()

        conn.close()

        # Step 5: Construct the full shortened URL
        shortened_url = f"https://myurl-ck9x.onrender.com/{short_code}"
        
        # Step 6: Return the shortened URL as a JSON response
        return jsonify({'shortened_url': shortened_url}), 200

    except sqlite3.Error as e:
        # Handle database related errors
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    except Exception as e:
        # Catch any general errors
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)


