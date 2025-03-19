#!/usr/bin/env python3
import sqlite3
import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Hardcoded credentials in the code
API_KEY = "sk_live_12345abcdefghijklmnop"
DB_PASSWORD = "admin123"
ADMIN_PASSWORD = "password123"

@app.route('/login', methods=['POST'])
def login():
    # No input validation or sanitization
    username = request.form['username']
    password = request.form['password']
    
    # SQL Injection vulnerability with string concatenation
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    # Plaintext password storage
    if password == ADMIN_PASSWORD:
        return "Login successful!"
    
    # Detailed error messages expose system information
    return f"Login failed! Debug info: Query was {query}, Server: {os.uname()}"

@app.route('/upload', methods=['POST'])
def upload_file():
    # No file validation
    file = request.files['file']
    # Path traversal vulnerability
    filename = request.form['filename']
    file.save(f'/uploads/{filename}')
    return "File uploaded!"

@app.route('/template', methods=['GET'])
def render_template():
    # Template injection vulnerability
    template = request.args.get('template', '{{name}}')
    name = request.args.get('name', 'Guest')
    # Rendering user input directly in template
    return render_template_string(template)

@app.route('/external', methods=['GET'])
def external_request():
    # Insecure HTTP communication
    url = request.args.get('url')
    # No validation of external URL
    response = requests.get(url, verify=False)
    return response.text

if __name__ == '__main__':
    # Running with debug=True in production
    # Exposing the app on all interfaces with no HTTPS
    app.run(host='0.0.0.0', port=80, debug=True)
