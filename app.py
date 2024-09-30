from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template_string('''
        <h2>Login Page</h2>
        <form action="/login" method="POST">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    blacklist = ["'", '"', "or", "and", "--", "#", ";"]
    
    if request.method == 'POST':
        if any(item.lower() in username.lower() or item.lower() in password.lower() for item in blacklist):
            return "Possible SQL Injection detected! Access Denied.", 403
    
    query = f'SELECT * FROM users WHERE username="{username}" AND password="{password}"'
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute(query)
    except sqlite3.Error as e:
        return f"SQL Error: {e}", 500

    user = c.fetchone()
    conn.close()

    if user:
        return 'Welcome, admin! Flag: CyberXbytes{2bbf311c73e9c87291783251049a3a95}'
    else:
        return "Invalid credentials."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
