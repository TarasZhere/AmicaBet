from flask import Blueprint, request, jsonify
from server.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/uid', methods=['POST'])
def register():
    user_id = request.json["Uid"]
    db = get_db()

    try:
        user = db.execute('SELECT * FROM user WHERE Uid = ?',
                          (user_id,)).fetchone()
        if user is None:
            return ('User not found', 404)
    except:
        return ('Internal error', 500)

    return jsonify(dict(user)), 200


@bp.route('/friends', methods=['POST'])
def get_friends():
    user_id = request.json['Uid']
    db = get_db()

    def checkStatus(rec_friend):
        friend = dict(rec_friend)
        if friend.get('status') == 'pending':
            friend['status'] = 'request'
        return friend

    try:
        received = db.execute(
            'SELECT Uid, fname, lname, email, status FROM (SELECT * FROM friendRequest WHERE receiver_Uid = ? AND (status != "blocked" AND status != "rejected")) AS friends, user AS u WHERE friends.sender_Uid = u.Uid', [
                user_id]
        ).fetchall()

        friends = list(map(lambda i: checkStatus(i), received))

        requested = db.execute(
            'SELECT Uid, fname, lname, email, status FROM (SELECT * FROM friendRequest WHERE sender_Uid = ? AND (status != "blocked" AND status != "rejected")) AS friends, user AS u WHERE friends.receiver_uid = u.Uid', [
                user_id]
        ).fetchall()

        list(map(lambda i: friends.append(dict(i)), requested))

    except Exception as e:

        return (e, 404)
    else:
        return jsonify(friends), 200
