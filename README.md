# Log Analyzer

## Overview

Log Analyzer is a web-based application that enables users to upload log files, analyze them for suspicious activity, and download an analyzed report. The tool is designed to identify patterns such as failed login attempts, authentication failures, access denials, and other irregularities, providing users with actionable insights into their log data.

---

## Features

- **User-Friendly Interface:** A simple and intuitive web interface for uploading log files and downloading reports.
- **Log Analysis:** Detects suspicious activities such as failed logins, access denials, and root user access.
- **Database Integration:** Stores metadata (user details and filenames) in a SQLite database for tracking uploads.
- **Real-Time Processing:** Analyzes logs immediately after upload and generates a report for download.

---

## How It Works

1. Users visit the web interface and upload their log file.
2. The file is securely stored in the backend.
3. A Python-based analysis engine scans the log file for suspicious patterns.
4. An analyzed log file is generated and made available for download.

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Database:** SQLite
- **Hosting Environment:** Localhost (development)

---

## Setup and Installation

### Prerequisites
- Python 3.x
- Flask (`pip install flask`)
- SQLite (comes pre-installed with Python)
- Git (for version control)

### Steps to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/gunanjr/Log-Analyzer.git
   cd Log-Analyzer

2. Install required dependencies:
    ```bash
    pip install flask

3. Initialize the database:
    ```bash
    python
    >>> from app import init_db
    >>> init_db()
    >>> exit()

4. Start the Flask server:
    ```bash
    python app.py

5. Open your browser and navigate to:
    ```arduino
    http://127.0.0.1:5000

Future Enhancements
  Add advanced log analysis using Machine Learning models.
  Deploy the application on a cloud platform like AWS or Heroku.
  Implement user authentication for secure file uploads.

Contributing
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

