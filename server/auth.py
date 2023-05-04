import functools

from amica.utils import validEmail, invalidPassword

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from amica.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cPassword = request.form.get('conf-password')
        fname = request.form.get('fname')
        lname = request.form.get('lname')

        error = None
        db = get_db()  

        if not validEmail(email):
            error = "Enter a valid Email"

        elif invalidPassword(password):
            error = invalidPassword(password)

        elif not password == cPassword:
            error = "Passwords do not match"

        if error is None:
            try:  
                db.execute(
                    "INSERT INTO user (email, password, fname, lname) VALUES (?, ?, ?, ?)",
                    (email, generate_password_hash(password), fname, lname),
                )
                db.commit()
            except:
                error = f"Email {email} is already registered."
            else:
                return render_template('auth/login.html', email=email)

        flash(error)

        return render_template('auth/register.html', user={
            'email':email,
            'fname':fname,
            'lname':lname,
        })
    return render_template('auth/register.html', user={
            'email':"",
            'fname':"",
            'lname':"",
        })


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('user.homepage'))

        flash(error)


    # redirect user in if it is already logged in.
    if g.user is not None:
        return redirect(url_for('user.homepage'))
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    try:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (session.get('user_id'),)
        ).fetchone()
    except:
        g.user = None


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view