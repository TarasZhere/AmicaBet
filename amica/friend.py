from flask import Blueprint, session, abort, request, render_template, redirect, url_for
from amica.auth import login_required
from amica.db import get_db
from .user import get_all_friends

bp = Blueprint('friend', __name__, url_prefix='/friend')


@bp.route('/')
@login_required
def index():
    db = get_db()

    try:
        user = db.execute('SELECT * FROM user WHERE Uid = ?',
                          (session.get('Uid'),)).fetchone()
        if user is None:
            Exception('User not found')
        else:
            user = dict(user)
    except:
        session.clear()
        return redirect(url_for('auth.login'))

    friends = get_all_friends()

    bets = []

    for friend in friends:
        f_Uid = friend.get('Uid')
        friend_bets = db.execute(
            'SELECT DISTINCT Bid FROM (SELECT * FROM bet, user, invite WHERE bet.Bid = invite.Bid and (invite.Uid = ? OR invite.invited_Uid = ?) ) ', (f_Uid, f_Uid)).fetchall()

        if friend_bets:
            for bet in friend_bets:
                bets.append(dict(bet).get('Bid'))

    print(bets)
    return render_template('user/friend.html', user=user, friends=friends, bets=bets)


@bp.route('add/<int:receiver_Uid>')
@login_required
def add(receiver_Uid):

    sender_Uid = session.get('Uid')
    db = get_db()

    try:
        db.execute(
            "INSERT INTO friendRequest (sender_Uid, receiver_Uid) VALUES (?, ?)", [
                sender_Uid, receiver_Uid
            ]
        )

        user_name = db.execute(
            "SELECT fname, lname FROM user WHERE Uid=?", [sender_Uid]).fetchone()

        user_name = dict(user_name)

        # add notification to receiver
        db.execute(
            "INSERT INTO notification (Uid, message) VALUES (?, ?)", [
                receiver_Uid, f'Friend request from {user_name["fname"]} {user_name["lname"]}.'
            ])

        db.commit()
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200


@bp.route('get/<int:friend_Uid>')
@login_required
def get_friend(friend_Uid):
    db = get_db()
    try:
        user = db.execute('SELECT Uid, fname, lname, balance, email FROM friendRequest as f, user as u WHERE status="accepted" AND (f.sender_Uid=? AND f.receiver_Uid=? AND u.Uid=?) OR (f.sender_Uid=? AND f.receiver_Uid=? AND u.Uid=?)', [
                          session.get('Uid'), friend_Uid, friend_Uid, friend_Uid, session.get('Uid'), friend_Uid]).fetchone()
    except Exception as e:
        print(e)
        abort(500)

    user = dict(user)
    return user, 200


@bp.route('accept', methods=['POST'])
@login_required
def accept():
    sender_Uid = request.json['sender_Uid']
    receiver_Uid = session.get('Uid')
    db = get_db()

    try:
        db.execute(
            'UPDATE friendRequest SET status="accepted" WHERE sender_Uid=? AND receiver_Uid=?', [sender_Uid, receiver_Uid])

        # add notification to sender
        user_name = db.execute(
            "SELECT fname, lname FROM user WHERE Uid=?", [receiver_Uid]).fetchone()

        user_name = dict(user_name)

        db.execute(
            "INSERT INTO notification (Uid, message) VALUES (?, ?)", [
                sender_Uid, f'{user_name["fname"]} {user_name["lname"]} accepted your friend request.'
            ])

        db.commit()
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200


@bp.route('reject', methods=['POST'])
@login_required
def reject():
    sender_Uid = request.json['sender_Uid']
    receiver_Uid = session.get('Uid')
    db = get_db()

    try:
        db.execute(
            'UPDATE friendRequest SET status="rejected" WHERE sender_Uid=? AND receiver_Uid=?', [sender_Uid, receiver_Uid])
        db.commit()
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200
