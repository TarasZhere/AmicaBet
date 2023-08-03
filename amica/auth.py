import functools
from amica.utils import validEmail, invalidPassword
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from amica.db import get_db

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
                db = get_db()
                db.execute(
                    "INSERT INTO user (email, password, fname, lname) VALUES (?, ?, ?, ?)",
                    (user['email'].lower(), generate_password_hash(
                        user['password']), user['fname'].lower(), user['lname'].lower()),
                )
                db.commit()
            except Exception as e:
                print(e)
                error = f"Email {user.get('email')} is already registered."
            else:
                user_id = db.execute("SELECT Uid FROM user WHERE email=? ",
                                     (user['email'],)).fetchone()

                user_id = dict(user_id).get('Uid')

                # adding default presidents as frieends
                db.execute(
                    "INSERT INTO friendRequest (sender_Uid, receiver_Uid, status) values (1, ?, 'pending'),(2, ?, 'pending'),(3, ?, 'pending');", [
                        user_id, user_id, user_id]
                )
                if user_id != 104:
                    db.execute(
                        "INSERT INTO friendRequest (sender_Uid, receiver_Uid, status) values (104, ?, 'pending')", [
                            user_id]
                    )

                db.commit()
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
        email = request.form['email'].lower()
        error = None
        try:
            db = get_db()
            user = db.execute(
                f'SELECT * FROM user WHERE email = ?', [email]
            ).fetchone()

            if user is None:
                error = 'User not found'

            else:
                user = dict(user)

                if not check_password_hash(user.get('password'), request.form['password']):
                    error = 'Incorrect password.'

        except Exception as e:
            print(e)
            error = 'Server error'

        if error is None:
            session['Uid'] = user.get('Uid')
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
