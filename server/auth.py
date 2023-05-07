from flask import (
    Blueprint, request, jsonify
)
from werkzeug.security import generate_password_hash
from server.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    try:
        db = get_db()
        db.execute(
            "INSERT INTO user (email, password, fname, lname) VALUES (?, ?, ?, ?)",
            (request.json['email'], generate_password_hash(
                request.json['password']), request.json['fname'], request.json['lname']),
        )
    except:
        return ('User already registerd', 400)

    user_id = db.execute("SELECT Uid FROM user WHERE email=? ",
                         (request.json['email'],)).fetchone()

    user_id = dict(user_id).get('Uid')

    # adding default presidents as frieends
    db.execute(
        "INSERT INTO friendRequest (sender_Uid, receiver_Uid, status) values (1, ?, 'accepted'),(2, ?, 'accepted'),(3, ?, 'accepted');", [
            user_id, user_id, user_id]
    )
    db.commit()

    return ('Registered', 200)


@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']

    try:
        db = get_db()
        user = db.execute(
            f'SELECT * FROM user WHERE email = ?', [email]
        ).fetchone()
    except:
        return 'Server error', 500

    if user is None:
        return 'User not found', 404

    user = dict(user)
    return jsonify(user), 200
