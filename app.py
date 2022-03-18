from quart import Quart, render_template, request


app = Quart(__name__)

@app.route('/')
async def home():
    return await render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        form = await request.form
        return form
    else:
        return "👀"

if __name__ == '__main__':
    app.run(debug=True)