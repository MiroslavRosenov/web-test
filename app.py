from quart import Quart, flash, redirect, render_template, request, session

app = Quart(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

VALID_CREDENTIALS = {
    "username": "admin",
    "password": "admin"
}

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

        if dict == VALID_CREDENTIALS:
            session["username"] = dict.get('username')
            session["logged"] = True
            
            return redirect("/")
        
        else:
            if dict.get('username') != VALID_CREDENTIALS.get('username'):
                await flash("Invalid username")
            
            if dict.get('password') != VALID_CREDENTIALS.get('password'):
                await flash("Invalid password")
    
            return await render_template("login.html", username=dict.get('username'), password=dict.get('password'))

if __name__ == '__main__':
    app.run(debug=True)