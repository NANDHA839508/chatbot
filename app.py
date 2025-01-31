import secrets
import openai
import os
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secure Random Secret Key
app.secret_key = secrets.token_hex(16)

# Load OpenAI API Key from Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you set this in your environment

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

@app.route('/signup')
def register():
    return render_template('signup.html')

@app.route('/login')
def welcome():
    return render_template('login.html')

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[1], password):  # Validate password securely
        session['user_id'] = user[0]  
        session['username'] = username
        flash("Login successful!", "success")
        return redirect(url_for('chat'))
    else:
        flash("Invalid username or password", "danger")
        return redirect(url_for('home'))

# Signup (Registration)
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    # Hash password before storing
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        flash("Username already exists", "danger")
        cur.close()
        return redirect(url_for('home'))

    cur.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", 
                (name, email, username, hashed_password))
    mysql.connection.commit()
    cur.close()

    flash("Registration successful! You can now login.", "success")
    return redirect(url_for('welcome'))

# Chat Page
@app.route('/chat')
def chat():
    if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('welcome'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_message, bot_response, timestamp FROM chat_history WHERE user_id = %s ORDER BY timestamp DESC", 
                (session['user_id'],))
    messages = cur.fetchall()
    cur.close()

    return render_template('chat.html', messages=messages)

# Sending Messages to OpenAI
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'})

    user_message = request.form['message'].strip()
    print("user message:", user_message)
    # Ensure message is not empty
    if not user_message:
        return jsonify({'bot_response': 'Message cannot be empty'})

    # OpenAI API request
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_response = response['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({'bot_response': 'Error fetching response from AI.'})

    # Store chat history in MySQL
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (%s, %s, %s)", 
                (session['user_id'], user_message, bot_response))
    mysql.connection.commit()
    cur.close()

    return jsonify({'bot_response': bot_response})

# Chat History API (For UI)
@app.route('/chat_history')
def chat_history():
    if 'user_id' not in session:
        return jsonify([])  # Empty response if not logged in

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_message, bot_response, timestamp FROM chat_history WHERE user_id = %s ORDER BY timestamp DESC", 
                (session['user_id'],))
    history = cur.fetchall()
    cur.close()

    return jsonify(history)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('welcome'))

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
