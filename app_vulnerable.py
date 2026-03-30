# app_vulnerable.py
"""
SQL Injection Practice - VULNERABLE VERSION
This app intentionally contains SQL injection vulnerabilities for educational purposes.
DO NOT use this code in production.
"""

from flask import Flask, render_template, request, session, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'test-secret-key-vulnerable'

# Initialize database with test users
def init_db():
    if os.path.exists('users.db'):
        os.remove('users.db')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute("INSERT INTO users VALUES (1, 'admin', 'password123')")
    c.execute("INSERT INTO users VALUES (2, 'user', 'user456')")
    c.execute("INSERT INTO users VALUES (3, 'guest', 'guest789')")
    conn.commit()
    conn.close()
    print("Database initialized with test users")

@app.route('/')
def index():
    return render_template('login.html', vulnerable=True)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    conn = sqlite3.connect('users.db')
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
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials', vulnerable=True)
    
    except sqlite3.OperationalError as e:
        conn.close()
        return render_template('login.html', error=f'Database error: {str(e)}', vulnerable=True)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', username=session['username'], vulnerable=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
