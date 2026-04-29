"""
WGU Construction Equipment Rental - Flask Application (Student Starter)

Scenario:
You have been provided with this partially operational web application.
While it "works" (the site loads and processes requests), it is fragile and insecure.
Previous logs (`network_security_log.txt`) indicate several issues:
1. Application crashes (Runtime Errors).
2. Security vulnerabilities (Unrestricted inputs, suspicious IPs).
3. Lack of real-time logging (Blind spots).

Your Task:
1. Analyze the `network_security_log.txt` to understand the past issues.
2. Review the `static_analysis_report.txt` to see vulnerabilities detected by
   static analysis tools (Flake8 and Bandit) - supports Rubric Aspect A9.
3. Modify this file (`app_student.py`) to:
   - Configure Python's logging module to write to 'Troubleshooting_studentID.log'.
   - Add defensive coding (Assertions, Try/Except blocks) to prevent crashes.
   - Add proper validation (e.g., check for negative days, invalid users).
   - Log all significant events (INFO) and errors (WARNING/ERROR).

Static Analysis Tools Used:
- Flake8: Code quality and PEP 8 style checking (run: python -m flake8 app_student.py)
- Bandit: Security vulnerability detection (run: python -m bandit app_student.py)
"""

# TODO: Import the logging module - Complete
import logging #added logging module
import ipaddress #added to validate ip format
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkeyforflasksessions'

# ------------------------------------------------------------
# TODO: Configure Logging Here - Complete
# Requirements:
# - Filename: 'Troubleshooting_studentID.log'
# - Level: INFO (capture INFO, WARNING, ERROR)
# - Format: '%(asctime)s - %(levelname)s - %(message)s'
# ------------------------------------------------------------
logging.basicConfig(
    filename='Troubleshooting_studentID.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Equipment Pricing Data
EQUIPMENT_PRICES = {
    "Bulldozer": 500,
    "Excavator": 450,
    "Crane": 800
}

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def validate_username(username):
    """
    Validates that the username is allowed.
    Currently insecure: it returns True for almost anything!
    """
    # TODO: Add assertions here to check if username is a string and not empty. - Complete
    assert isinstance(username, str), "Validation failed: Username must be a string."
    assert len(username.strip()) > 0, "Validation failed: Username must not be empty."
    logging.info(f"ASSERTION SUCCESS: Username '{username}' passed string validation.")
    allowed_users = {"admin", "alice", "bob", "charlie"}
    if username in allowed_users:
        return True
    return False

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

@app.route('/')
def home():
    # TODO: Log "Home page accessed" at INFO level - Complete
    logging.info("Home page accessed") # Replaced with logger
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Simulated IP address (In a real app, this would be request.remote_addr)
        ip_address = request.remote_addr 
        
        # TODO: Add defensive check (Assertion) to validate ip_address format (e.g., not None, valid string format) - Complete
        assert ip_address is not None, "Defensive Error: IP address was not provided."
        assert isinstance(ip_address, str), "Defensive Error: IP address must be a string."

        try:
            ipaddress.ip_address(ip_address)
            is_valid = True
        except ValueError:
            is_valid = False
        assert is_valid, f"Defensive Error: '{ip_address}' is not a valid IP format."

        # TODO: Check for Suspicious IP (e.g., external IPs not starting with "192.168." or "10.") and log a WARNING - Complete
        # Check for suspicious IPs
        if not (ip_address.startswith("192.168.") or ip_address.startswith("10.")):
            logging.warning(f"SUSPICIOUS IP DETECTED | IP: {ip_address} | User: {username}")

        # TODO: Log the login attempt details (username and IP) - Complete
        if validate_username(username):
            logging.info(f"LOGIN SUCCESS | User: {username} | IP: {ip_address}")
        else:
            logging.warning(f"LOGIN FAILED | User: {username} | IP: {ip_address}")
            return "Access Denied", 401
        
        # Authentication Logic
        if validate_username(username) and password == "secret123":
            # TODO: Log successful login - Complete
            logging.info(f"User {username} logged in.") 
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('home'))
        else:
            # TODO: Log failed login (WARNING) - Complete
            logging.warning(f"Login failed for {username}.")
            flash("Invalid credentials.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/rent', methods=['GET', 'POST'])
def rent_equipment():
    rental_result = None
    
    if request.method == 'POST':
        equipment_type = request.form.get("equipment_type")
        days_str = request.form.get("days")

        # TODO: Log the rental request details - Complete
        logging.info(f"RENTAL REQUEST | Equipment: {equipment_type} | Days: {days_str}")

        # --- VULNERABLE SECTION START ---
        # TODO: Wrap this section in a try/except block to catch crashes (ValueError, etc.) - Complete
        try:
        # Potential Crash: What if equipment_type is not in the dictionary?
            if equipment_type not in EQUIPMENT_PRICES:
                raise KeyError(f"Invalid equipment type: {equipment_type}")
            daily_rate = EQUIPMENT_PRICES[equipment_type]
        
        # Potential Crash: What if days_str is "abc"? (ValueError) - Complete
            if days_str.isdigit():
                days = int(days_str)
            else:
                raise ValueError("Days is not a valid number.")
        
        # Logic Defect: What if days is -5? It currently calculates a negative cost!
        # TODO: Add an assertion or check to ensure days > 0 - Complete
            assert days > 0, "Rental days must be greater than zero."
            logging.info(f"ASSERTION SUCCESS: Rental days ({days}) validated as a positive integer.")
            total_cost = daily_rate * days
        
        # TODO: Log the successful calculation (INFO) - Complete
            logging.info(f"RENTAL CALCULATION SUCCESS | Calculated cost: {total_cost}")

            rental_result = {
                "equipment": equipment_type,
                "days": days,
                "total_cost": total_cost
            }
            flash("Rental calculated successfully!", "success")
        
        # --- VULNERABLE SECTION END ---
        
        # TODO: In your except blocks, log the errors (ERROR) and flash a user-friendly message - Complete
        except (ValueError, KeyError, AssertionError) as e:
            logging.error(f"RENTAL ERROR | Error processing rental: {str(e)}")
            flash("Something went wrong. Please try again.", "danger")
    return render_template('rent.html', rental_result=rental_result)

if __name__ == '__main__':
    logging.info("Starting application...")# Replaced with logger
    app.run(debug=False, port=5000)