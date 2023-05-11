from flask import Blueprint, request, jsonify
from server.db import get_db

bp = Blueprint('bet', __name__, url_prefix='/bet')


@bp.route('/', methods=['POST'])
def getBets():
    user_id = request.json["Uid"]
    status = dict(request.json).get('status')

    if status == None:
        query = "SELECT * FROM bet AS b, (SELECT * FROM invite WHERE Uid = ? OR invited_Uid = ?) AS i WHERE b.Bid = i.Bid", [
            user_id, user_id]

    elif status == 'pending' or status == 'rejected':
        query = "SELECT * FROM bet AS b, (SELECT * FROM invite WHERE (Uid = ? OR invited_Uid = ?) AND status = ?) AS i WHERE b.Bid = i.Bid;", [
            user_id, user_id, status]

    elif status == 'partecipate':
        query = "SELECT * FROM bet AS b, (SELECT * FROM invite WHERE Uid = ? OR invited_Uid = ?) AS i WHERE b.Bid = i.Bid AND b.status = 'running'", [
            user_id, user_id]

    elif status == 'won':
        query = "SELECT * FROM bet AS b, (SELECT Bid FROM win WHERE Uid = ?) AS w WHERE b.Bid = w.Bid;", [
            user_id]

    elif status == 'lost':
        query = "SELECT * FROM bet AS b, (SELECT Bid FROM partecipate WHERE Uid=? AND Uid NOT IN (SELECT Uid FROM win WHERE Uid=?)) AS p WHERE b.status='closed'", [
            user_id, user_id]

    try:
        db = get_db()
        bets = db.execute(*query).fetchall()
    except Exception as e:
        print(e)
        return (str(e), 500)

    bets = list(map(lambda i: dict(i), bets))

    return jsonify(bets), 200


@bp.route('/create', methods=['POST'])
def create():
    bet = request.get_json()
    db = get_db()

    try:

        db.execute(
            'UPDATE user SET balance=balance-? WHERE Uid=?', [bet.get('ticket'), bet.get('Uid')])

        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bet (title, description, ticket) VALUES (?, ?, ?)', [
                bet.get('title').lower(), bet.get('description').lower(), bet.get('ticket')]
        )

        Bid = cursor.lastrowid
        db.execute(
            'INSERT INTO invite (Bid, Uid, invited_Uid) VALUES (?, ?, ?)', [
                Bid, bet.get('Uid'), bet.get('invited_Uid')]
        )

        db.commit()
    except Exception as e:
        print(e)
        return e, 500

    return 'Ok', 200


@bp.route('/accept/<int:Bid>')
def accept(Bid):
    db = get_db()

    try:
        # update the status of the invite
        db.execute(
            'UPDATE invite SET status = "accepted" WHERE Bid = ?', [Bid])

        db.execute(f'''
        UPDATE user
        SET balance = balance - b.ticket
        FROM (
            SELECT b.ticket AS ticket, i.invited_Uid as Uid
            FROM invite AS i, bet AS b
            WHERE b.Bid = ? AND i.Bid = b.Bid
        ) b
        WHERE user.Uid = b.Uid
        ''', [Bid])

        db.execute(
            'UPDATE bet SET status = "running" WHERE Bid = ?', [Bid])

        db.commit()
    except Exception as e:
        print(e)
        return e, 500

    return 'OK', 200
