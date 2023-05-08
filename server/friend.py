from flask import Blueprint, request, jsonify, abort
from server.db import get_db

bp = Blueprint('friend', __name__, url_prefix='/friend')


@bp.route('search/', methods=['POST'])
@bp.route('search/<string:input_search>', methods=['POST'])
def searchfriend(input_search=""):
    db = get_db()
    cursor = db.cursor()
    Uid = request.json['Uid']
    input_search = input_search.lower()

    try:
        query = f"SELECT Uid, fname, lname, email FROM user WHERE (fname LIKE ? OR lname LIKE ?) AND Uid NOT IN (SELECT sender_Uid FROM friendRequest WHERE sender_Uid={Uid} OR receiver_Uid={Uid}) AND Uid NOT IN (SELECT receiver_Uid FROM friendRequest WHERE sender_Uid={Uid} OR receiver_Uid={Uid})"

        cursor.execute(query, ('%' + input_search +
                       '%', '%' + input_search + '%'))
        users = cursor.fetchall()
        cursor.close()

    except Exception as e:
        print(e)
        abort(500)
    else:
        users = list(map(lambda i: dict(i), users))

    return jsonify(users), 200


@bp.route('/add', methods=['POST'])
def addfriend():
    sender_Uid = request.json['Uid']
    receiver_Uid = request.json['receiver_Uid']
    db = get_db()

    try:
        db.execute(
            "INSERT INTO friendRequest (sender_Uid, receiver_Uid) VALUES (?, ?)", [
                sender_Uid, receiver_Uid
            ]
        )

        db.commit()
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200


@bp.route('accept', methods=['POST'])
def accept():
    sender_Uid = request.json['sender_Uid']
    receiver_Uid = request.json['receiver_Uid']

    db = get_db()

    try:
        db.execute(
            'UPDATE friendRequest SET status="accepted" WHERE sender_Uid=? AND receiver_Uid=?', [sender_Uid, receiver_Uid])
        db.commit()
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200


@bp.route('reject', methods=['POST'])
def reject():
    sender_Uid = request.json['sender_Uid']
    receiver_Uid = request.json['receiver_Uid']

    db = get_db()

    try:
        db.execute(
            'UPDATE friendRequest SET status="rejected" WHERE sender_Uid=? AND receiver_Uid=?', [sender_Uid, receiver_Uid])
        db.commit()
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200
