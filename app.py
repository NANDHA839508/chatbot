import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Generate a secure, random secret key
app.secret_key = secrets.token_hex(16)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chatbot'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup')
def register():
    return render_template('signup.html')

@app.route('/login')
def Welcome():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        flash("Login successful!", "success")
        return redirect(url_for('chat'))
    else:
        flash("Invalid username or password", "danger")
        return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
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

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.form['message']
        response = generate_response(user_message)
        return render_template('chat.html', user_message=user_message, response=response)
    return render_template('chat.html', user_message=None, response=None)

def generate_response(message):
    # Basic command-based responses
    commands = {
        "hello": "Hello! How can I assist you?",
        "help": "Here are some commands you can try: hello, help, exit.",
        "exit": "Goodbye! Have a great day!",
    }
    return commands.get(message.lower(), "Sorry, I didn't understand that. Try typing 'help'.")

if __name__ == '__main__':
    app.run(debug=True)
