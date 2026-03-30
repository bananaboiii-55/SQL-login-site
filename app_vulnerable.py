# app_vulnerable.py
"""
SQL Injection Practice - VULNERABLE VERSION
This app intentionally contains SQL injection vulnerabilities for educational purposes.
DO NOT use this code in production.
"""

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os
import sys

app = Flask(__name__)
app.secret_key = 'test-secret-key-vulnerable-12345'

DATABASE = 'users.db'

# Initialize database with test users
def init_db():
    """Create database and populate with test users"""
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE users
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        c.execute("INSERT INTO users VALUES (1, 'admin', 'password123')")
        c.execute("INSERT INTO users VALUES (2, 'user', 'user456')")
        c.execute("INSERT INTO users VALUES (3, 'guest', 'guest789')")
        conn.commit()
        conn.close()
        print("✓ Vulnerable database initialized with test users")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)

@app.route('/')
def index():
    """Render login page"""
    return render_template('login.html', vulnerable=True)

@app.route('/login', methods=['POST'])
def login():
    """Handle login - VULNERABLE to SQL injection"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # VULNERABLE: Direct string concatenation allows SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[VULNERABLE] Executing query: {query}")
    
    try:
        c.execute(query)
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials', vulnerable=True)
    
    except sqlite3.OperationalError as e:
        conn.close()
        error_msg = f'Database error: {str(e)}'
        print(f"[ERROR] {error_msg}")
        return render_template('login.html', error=error_msg, vulnerable=True)

@app.route('/dashboard')
def dashboard():
    """Display dashboard - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'], vulnerable=True)

@app.route('/logout')
def logout():
    """Handle logout"""
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('login.html', error='Page not found', vulnerable=True), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('login.html', error='Server error', vulnerable=True), 500

if __name__ == '__main__':
    init_db()
    print("\n" + "="*60)
    print("SQL Injection Practice Lab - VULNERABLE VERSION")
    print("="*60)
    print("⚠️  WARNING: This version is intentionally vulnerable!")
    print("🔗 Running on http://0.0.0.0:5000")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
