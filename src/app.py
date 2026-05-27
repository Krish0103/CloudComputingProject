from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash
import sqlite3
import bcrypt
import jwt
import os
import datetime
from functools import wraps
from dotenv import load_dotenv

from password_checker import check_password
from login_monitor import record_login_attempt, is_brute_force, generate_security_alert

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'cyber-sec-super-secret-key-2026')

def get_db_connection():
    try:
        conn = sqlite3.connect('cybersec.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

init_db()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login'))
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['userId']
        except jwt.ExpiredSignatureError:
            flash("Session expired, please log in again.", "error")
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            flash("Invalid session, please log in again.", "error")
            return redirect(url_for('login'))
        
        return f(current_user_id, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username and password required', 'error')
        return redirect(url_for('register'))

    # Check password strength
    strength = check_password(password)
    if strength['summary'] not in ('Strong', 'Medium') or strength['weak_password']:
        flash(f"Password is too {strength['summary']}. Ensure it has 8+ characters, uppercase, lowercase, numbers, and special characters.", 'error')
        return redirect(url_for('register'))

    conn = get_db_connection()
    if not conn:
        flash('Database not reachable', 'error')
        return redirect(url_for('register'))

    try:
        cursor = conn.cursor()
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            flash('User already exists', 'error')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insert user
        cursor.execute("INSERT INTO users (username, password, password_hash) VALUES (?, ?, ?)", (username, password, hashed_password))
        conn.commit()
        flash('User registered successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash(f'Registration error: {str(e)}', 'error')
        return redirect(url_for('register'))
    finally:
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    login_type = request.form.get('type') # 'vulnerable' or 'secure'

    if not username or not password:
        flash('Username and password required', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    if not conn:
        flash('Database not reachable', 'error')
        return redirect(url_for('login'))

    try:
        cursor = conn.cursor()
        if login_type == 'vulnerable':
            # VULNERABLE LOGIN
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                flash('Vulnerable login succeeded. (No JWT returned)', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials', 'error')
                return redirect(url_for('login'))
        else:
            # SECURE LOGIN
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                record_login_attempt(username, True, 'Login successful')
                token = jwt.encode({
                    'userId': user['id'],
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
                }, app.config['SECRET_KEY'], algorithm="HS256")
                
                response = make_response(redirect(url_for('dashboard')))
                response.set_cookie('token', token, httponly=True)
                flash('Secure login succeeded.', 'success')
                return response
            else:
                record_login_attempt(username, False, 'Invalid credentials')
                if is_brute_force(username):
                    alert = generate_security_alert(username, 3)
                    record_login_attempt(username, False, 'Security alert triggered')
                    flash(alert, 'error')
                flash('Invalid credentials', 'error')
                return redirect(url_for('login'))

    except Exception as e:
        flash(f"Database error: {str(e)}", 'error')
        return redirect(url_for('login'))
    finally:
        conn.close()

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', '', expires=0)
    flash('Logged out successfully.', 'success')
    return response

@app.route('/profile/vulnerable/<int:profile_id>')
def profile_vulnerable(profile_id):
    # IDOR Vulnerability: No authentication check, no authorization check!
    # Anyone can view any user's data just by guessing their ID.
    conn = get_db_connection()
    if not conn:
        return "Database error", 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, created_at FROM users WHERE id = ?", (profile_id,))
        user = cursor.fetchone()
        if user:
            return f"<h2>Vulnerable Profile View</h2><p>User: <b>{user['username']}</b></p><p>Joined: {user['created_at']}</p>"
        return "User not found", 404
    finally:
        conn.close()

@app.route('/profile/secure/<int:profile_id>')
@token_required
def profile_secure(current_user_id, profile_id):
    # Secure: User must be logged in (token_required) AND authorized for this specific ID
    if current_user_id != profile_id:
        return "<h2>403 - Forbidden</h2><p>Unauthorized Access! You can only view your own profile.</p>", 403
        
    conn = get_db_connection()
    if not conn:
        return "Database error", 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, created_at FROM users WHERE id = ?", (profile_id,))
        user = cursor.fetchone()
        if user:
            return f"<h2>Secure Profile View</h2><p>User: <b>{user['username']}</b></p><p>Joined: {user['created_at']}</p>"
        return "User not found", 404
    finally:
        conn.close()

@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user_id):
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard.html', error='Database not reachable')

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, created_at FROM users WHERE id = ?", (current_user_id,))
        user = cursor.fetchone()
        
        return render_template('dashboard.html', user=user)
    except Exception as e:
        return render_template('dashboard.html', error=str(e))
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)