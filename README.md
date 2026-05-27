# 🛡️ SecureWeb Vulnerability Lab

Welcome to the **SecureWeb Vulnerability Lab**, a comprehensive, interactive web application built with Python and Flask. This project serves as an educational cybersecurity platform designed to demonstrate both common web vulnerabilities and robust defensive programming techniques.

## 📖 Project Overview

Originally starting as a decoupled API and frontend, this application has evolved into a secure monolithic **Flask** application. It embraces a "No-JS" philosophy for the frontend, relying entirely on advanced CSS for styling and animations, thereby reducing client-side attack surfaces.

The lab provides hands-on demonstrations of attacks like **SQL Injection (SQLi)**, **Cross-Site Scripting (XSS)**, and **Insecure Direct Object Reference (IDOR)**, alongside implementing custom offline security mechanisms such as password strength validation and brute-force login monitoring.

---

## ✨ Key Features & Defensive Mechanisms

1. **Secure Authentication Flow**
   - Uses `bcrypt` for secure password hashing and salting.
   - Issues **JSON Web Tokens (JWT)** for session management.
   - Tokens are stored in `HttpOnly` cookies, making them inaccessible to client-side scripts (mitigating XSS session hijacking).

2. **Custom Password Strength Enforcement**
   - Validates passwords against strict complexity rules (uppercase, lowercase, numbers, special characters, and minimum length).
   - Rejects common/weak dictionary passwords (e.g., "password", "12345").

3. **Brute-Force Defense & Logging**
   - Monitors and logs all login attempts (successes and failures) locally to `logs.txt`.
   - Analyzes recent attempts to detect brute-force attacks (e.g., 3 failed attempts in a short timeframe).
   - Dynamically triggers Security Alerts to warn the user/admin of suspicious activity.

4. **Zero-Configuration Database**
   - Uses a self-contained `SQLite3` database (`cybersec.db`) that auto-initializes using `setup.sql`.
   - Implements parameterized queries (`?`) to prevent SQL Injection in authenticated routes.

5. **JS-Free Frontend**
   - Responsive layouts (CSS Grid/Flexbox).
   - Interactive UI and simulated terminal typing animations using pure CSS keyframes (`styles.css`), completely stripping out JavaScript dependencies.

---

## 📂 Codebase Detail: What's inside?

The source code is located in the `src/` directory.

### Backend Configurations
- **`app.py`**: The heart of the monolithic application. It contains:
  - Database initialization (`init_db`) which safely builds tables on first run.
  - The `@token_required` decorator that intercepts and verifies JWT `HttpOnly` cookies on protected routes.
  - Routing logic for rendering Jinja templates (`render_template`).
  - Integration of offline security checks inside `/register` and `/login`.
- **`password_checker.py`**: A standalone script that validates password criteria via Regular Expressions (Regex). It returns a security score (Strong, Medium, Weak) and blocks compromised passwords.
- **`login_monitor.py`**: A dedicated monitoring module. It provides `record_login_attempt()` to write out local audit logs and `is_brute_force()` to parse those logs and detect rapid-fire failed authentication events.
- **`setup.sql`**: The SQL schema file defining the SQLite database layout (e.g., user tables with password_hash columns).

### Frontend Presentation
- **`templates/` folder**: Contains HTML files (`index.html`, `register.html`, `login.html`, `dashboard.html`). 
  - These use **Jinja2** templating to loop through and display backend `flash` messages (like Brute Force alerts or registration success prompts).
  - Escapes user inputs using standard Jinja syntax to mitigate XSS vulnerabilities natively.
- **`static/styles.css`**: The design engine. Handles CSS variables, hover effects, multi-column dynamic grids (`auto-fit`), and custom `.typing-line` animations.

---

## 🚀 How to Run the Project

1. **Install Dependencies**
   Navigate to the `src` folder and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have Flask, PyJWT, bcrypt, and python-dotenv installed).*

2. **Start the Flask Server**
   Run the main application file:
   ```bash
   python app.py
   ```

3. **Access the Web App**
   Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

## 🧪 Testing the Security Features
- **Test Password Rules**: Go to the `/register` page and attempt to register with the password `admin`. You will be blocked.
- **Test Brute Force Detection**: Go to the `/login` page and enter invalid credentials for a user 3 times in a row. A red security alert will be flashed to the screen!
- **Play with Vulnerabilities**: Look for the specific vulnerable endpoints created for educational purposes (SQLi, IDOR, XSS) to see how bad actors exploit unprotected inputs.
