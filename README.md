# Full-Stack Security Audit & Incident Logging System Project

## Project Overview
This project involves securing and stabilizing a legacy Flask-based web application for an equipment rental service. The initial application was found to be fragile, insecure, and lacked proper monitoring capabilities. 

Based on manual code review, static analysis (Flake8/Bandit), and network security log analysis, several critical vulnerabilities and reliability issues were identified and addressed.

## Identified Issues & Security Warnings

### 1. Hardcoded Administrative Credentials (CWE-259)
* **The Issue:** The application contained a hardcoded password (`"secret123"`) and secret key (`'supersecretkey...'`) directly in the source code.
* **Relevance:** This allows anyone with read access to the code to bypass authentication or forge session cookies.
* **Identification:** Found via **Bandit (B105)** at lines 25 and 85.

### 2. Missing Input Validation & Error Handling
* **The Issue:** User inputs for `equipment_type` and `days` were processed without validation or `try/except` blocks.
* **Relevance:** Entering non-numeric data or invalid equipment names caused the application to crash (`ValueError` or `KeyError`), leading to a Denial of Service (DoS).
* **Identification:** Found through **Manual Code Review** and verified by `ValueError` entries in the network logs.

### 3. Logic Defect: Negative Rental Days
* **The Issue:** The calculation `total_cost = daily_rate * days` did not check for negative integers.
* **Relevance:** Attackers could exploit this to generate negative costs (refunds) or corrupt financial totals.
* **Identification:** Found through **Manual Logic Analysis** and confirmed by `AssertionError` logs.

### 4. Absence of Persistent Logging (Blind Spots)
* **The Issue:** The app used `print()` statements for security-sensitive events.
* **Relevance:** `print()` output is ephemeral and lacks metadata (timestamps, levels). Without a log file, forensic analysis after a breach is impossible.
* **Identification:** Identified by the presence of `print()` placeholders and missing `logging` module configuration.

### 5. Insecure Infrastructure & Lack of Rate Limiting
* **The Issue:** The application lacked protection against automated brute-force attacks.
* **Relevance:** Network logs confirmed successful brute-force attempts from suspicious external IPs.
* **Identification:** Discovered by analyzing the `network_security_log.txt` showing multiple failed attempts in short durations.

## Technical Specifications & Remediation
To resolve these issues, the following modifications were implemented:
- **Logging Configuration:** Python’s `logging` module was configured to write to `Troubleshooting_studentID.log` with an `INFO` level and specific formatting.
- **Defensive Coding:** Added `try/except` blocks to the `/rent` route and `assertions` to the `validate_username` and rental logic.
- **Input Sanitization:** Implemented checks to ensure `days > 0` and that the `equipment_type` exists within the price dictionary before access.

## How to Run
1. Install dependencies:
       <br>Install Python `https://www.python.org/downloads/`
       <br>-`pip install flask`
       <br>-`pip install pytest`
       <br>-`pip install requests`


3. Run the application: `python app_student.py`
4. Run the tests to see if they passed: `pytest test_app.py` or `python -m pytest test_app.py`
5. Static Analysis:
    - Run Flake8: `python -m flake8 app_student.py`
    - Run Bandit: `python -m bandit app_student.py`
  
### Project Security Report
[![Security Report Preview](./images/pdf_preview.png)](./security-testing-python.pdf)
*Click the image above to open the full PDF report.*
