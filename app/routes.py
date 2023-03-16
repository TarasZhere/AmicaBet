from app import app
from flask import render_template, redirect, url_for, flash, request

@app.route('/index')
@app.route('/')
def index():
    users = [
        {'name':'tom'},
        {'name':'tim'},
        {'name':'jack'},
        {'name':'bob'},
    ]
    return render_template('index.html', title="home", users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        pass
      
    return render_template('login.html', title='Login')
    