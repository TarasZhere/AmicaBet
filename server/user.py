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

    try:
        requested = db.execute(
            'SELECT fname, lname, balance FROM (SELECT * FROM friendRequest WHERE sender_Uid = ? AND status = "accepted") AS friends, user AS u WHERE friends.receiver_uid = u.Uid', [
                user_id]
        ).fetchall()

        friends = list(map(lambda i: dict(i), requested))

        received = db.execute(
            'SELECT fname, lname, balance FROM (SELECT * FROM friendRequest WHERE receiver_Uid = ? AND status = "accepted") AS friends, user AS u WHERE friends.sender_Uid = u.Uid', [
                user_id]
        ).fetchall()

        list(map(lambda i: friends.append(dict(i)), received))

    except Exception as e:

        return (e, 404)
    else:
        return jsonify(friends), 200
