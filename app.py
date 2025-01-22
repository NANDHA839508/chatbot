import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Generate a secure, random secret key
app.secret_key = secrets.token_hex(16)  # Generates a 32-character hex string

# MySQL configuration (replace with your own database details)
app.config['MYSQL_HOST'] = 'localhost'  # Your MySQL server host
app.config['MYSQL_USER'] = 'root'       # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'chatbot'  # Your database name

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Welcome')
def Welcome():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    print (user)
    cur.close()

    if user:
        flash("Login successful!", "success")
        return redirect(url_for('Welcome'))
    else:
        flash("Invalid username or password", "danger")
        return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        flash("Username already exists", "danger")
        cur.close()
        return redirect(url_for('home'))

    cur.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", 
                (name, email, username, password))
    mysql.connection.commit()
    cur.close()

    flash("Registration successful! You can now login.", "success")
    return redirect(url_for('Welcome'))


if __name__ == '__main__':
    app.run(debug=True)
