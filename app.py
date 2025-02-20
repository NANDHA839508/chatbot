import secrets
import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Secure Random Secret Key
app.secret_key = secrets.token_hex(16)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chatbot'

mysql = MySQL(app)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Signup Page
@app.route('/signup')
def register():
    return render_template('signup.html')


@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/investment')
def invesment():
    return render_template('investment.html')

@app.route('/Long-term investment')
def longterm():
    return render_template('Long-term.html')


@app.route('/Short-term Investment')
def shortterm():
    return render_template('Short-term.html')


@app.route('/Stock-Price')
def stocprice():
    return render_template('Stock-Price.html')


@app.route('/login')
def welcome():
    return render_template('login.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


# ✅ Login Route (No Password Hashing)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required."}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user:
        stored_password = user[1]  # Get plain-text password from database

        print(f"DEBUG: Stored Password -> {stored_password}")  # Debugging
        print(f"DEBUG: Entered Password -> {password}")  # Debugging

        if stored_password == password:  # ✅ Plain text password comparison
            session['id'] = user[0]  
            session['username'] = username  
            return jsonify({"success": True, "message": "Login successful!", "redirect": "/chat"})  
        else:
            return jsonify({"success": False, "message": "Invalid password."}), 401
    else:
        return jsonify( {"success": False, "message": "Invalid username."}), 401

# ✅ Signup (No Password Hashing)
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']  # ✅ Store plain text password

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        flash("Username already exists", "danger")
        cur.close()
        return redirect(url_for('login'))

    cur.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", 
                (name, email, username, password))  # ✅ Storing plain text password
    mysql.connection.commit()
    cur.close()

    flash("Registration successful! You can now login.", "success")
    return redirect(url_for('login'))

# ✅ Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Run Flask App
if __name__ == '__main__':  
    app.run(debug=True)
