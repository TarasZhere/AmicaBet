from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    users = [
        {'name':'tom'},
        {'name':'tim'},
        {'name':'jack'},
        {'name':'bob'},
    ]
    return render_template('index.html', title="home", users=users)