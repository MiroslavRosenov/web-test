import sqlite3
from quart import Quart, flash, redirect, render_template, abort, request, session
from werkzeug.exceptions import HTTPException

app = Quart(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

conn = sqlite3.connect("database.db")

@app.errorhandler(HTTPException)
async def error_handler(error: HTTPException):
    if error.code == 400:
        return "Bruh, what is you doing 👀", error.code
    
    if error.code == 403:
        return "You are not allowed to be here", error.code
    
    if error.code == 404:
        return "Sorry, page not found!", error.code
    
    if error.code >= 500:
        return {error.code: error.description}, error.code

@app.route('/')
async def index():
    if not session.get('logged', False):
        return await render_template("login.html")
    return await render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'GET':
        return await render_template("login.html")
    
    if request.method == 'POST':
        dict = (await request.form).to_dict()

        username = dict.get('username')
        password = dict.get('password')

        if not username or not password:
            await flash("Please enter all required credentials")
            return await render_template("login.html", username=username, password=password)

        query = f"SELECT username, password FROM users WHERE username = '{username}' and password = '{password}';"
        cursor = conn.cursor()
        cursor.execute(query)
        
        if cursor.fetchone():
            session["username"] = username
            session["logged"] = True
            return redirect("/")
        
        else:
            await flash("Invalid credentials")
            return await render_template("login.html", username=username, password=password)

@app.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == "GET":
        return await render_template("register.html")

    elif request.method == "POST":
        dict = (await request.form).to_dict()

        username = dict.get('username')
        password = dict.get('password')

        if not username or not password:
            await flash("Please enter all required credentials")
            return await render_template("register.html", username=username, password=password)

        query = f"SELECT username, password FROM users WHERE username = '{username}';"
        cursor = conn.cursor()
        cursor.execute(query)
        
        if (cursor.fetchall()):
            cursor.close()
            await flash("There is already account with this username")
            return await render_template("register.html", username=username, password=password)
        else:
            query = f"INSERT INTO users VALUES ('{username}', '{password}');"
            cursor.execute(query)
            conn.commit()

            session["username"] = username
            session["logged"] = True
            return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)