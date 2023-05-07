from flask import Blueprint, request, jsonify
from server.db import get_db

bp = Blueprint('friend', __name__, url_prefix='/friend')


@bp.route('search/', methods=['POST'])
@bp.route('search/<string:input_search>', methods=['POST'])
def searchfriend(input_search=None):
    db = get_db()
    cursor = db.cursor()
    uid = request.json['Uid']

    try:
        query = f"SELECT DISTINCT Uid, fname, lname, email FROM (SELECT * FROM user, friendRequest WHERE (sender_Uid != {uid} AND receiver_Uid != {uid}) AND (Uid = sender_Uid OR Uid = receiver_Uid)) WHERE fname LIKE ? OR lname LIKE ?"
        cursor.execute(query, ('%' + input_search +
                       '%', '%' + input_search + '%'))
        users = cursor.fetchall()
        cursor.close()

    except Exception as e:
        return e, 500
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
        return e, 500

    return 'Ok', 200
