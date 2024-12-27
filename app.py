from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import os
import sqlite3
import uuid
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ANALYZED_FOLDER'] = 'analyzed'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['ANALYZED_FOLDER']):
    os.makedirs(app.config['ANALYZED_FOLDER'])

DATABASE = 'log_analyzer.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id TEXT PRIMARY KEY, name TEXT, filename TEXT)''')
    conn.commit()
    conn.close()

def analyze_log_file(input_path, output_path):
    suspicious_patterns = [
        r"Failed password for",           # Failed login attempts
        r"authentication failure",        # Authentication failures
        r"Invalid user",                  # Invalid user attempts
        r"error",                         # General errors
        r"denied",                        # Access denied
        r"session opened for user root",  # Root access
    ]

    with open(input_path, 'r') as f:
        log_content = f.readlines()

    suspicious_logs = []
    for line in log_content:
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in suspicious_patterns):
            suspicious_logs.append(line)

    if not suspicious_logs:
        analyzed_content = "No suspicious activity found in the log file."
    else:
        analyzed_content = "\n".join(suspicious_logs)

    with open(output_path, 'w') as f:
        f.write(analyzed_content)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form['name']
    file = request.files['logFile']
    if file:
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO logs (id, name, filename) VALUES (?, ?, ?)", 
                  (file_id, name, filename))
        conn.commit()
        conn.close()

        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f'analyzed_{filename}'
        output_path = os.path.join(app.config['ANALYZED_FOLDER'], output_filename)

        analyze_log_file(input_path, output_path)

        download_url = f'/download/{output_filename}'
        return jsonify(success=True, downloadUrl=download_url)
    else:
        return jsonify(success=False, message="No file uploaded")

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['ANALYZED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
