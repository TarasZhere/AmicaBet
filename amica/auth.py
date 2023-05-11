import functools
from amica.utils import validEmail, invalidPassword
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from requests import post
from amica.server_url import SERVER_URL as URL, headers


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = dict(request.form)
        error = None

        if not validEmail(user.get('email')):
            error = "Enter a valid Email"

        elif invalidPassword(user.get('password')):
            error = invalidPassword(user.get('password'))

        elif not user.get('password') == user.get('conf-password'):
            error = "Passwords do not match"

        if error is None:
            try:
                response = post(URL+'auth/register',
                                json=user, headers=headers)
                response.raise_for_status()
            except:
                error = f"Email {user.get('email')} is already registered."
            else:
                return render_template('auth/login.html', email=user.get('email'))

        flash(error)

        return render_template('auth/register.html', user=user)

    return render_template('auth/register.html', user={
        'email': "",
        'fname': "",
        'lname': "",
    })


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        try:
            response = post(
                URL+"auth/login", json={"email": request.form['email']}, headers=headers)

            if response.status_code == 404:
                error = f'User not found'

            elif not check_password_hash(response.json()['password'], request.form['password']):
                error = 'Incorrect password.'
        except Exception as e:
            print(e)
            error = 'Server error'

        if error is None:
            session['Uid'] = response.json()['Uid']
            return redirect(url_for('user.homepage'))

        flash(error)

    if session.get('Uid') is not None:
        return redirect(url_for('user.homepage'))
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('Uid') is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
