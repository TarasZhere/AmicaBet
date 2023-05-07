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
        query = "SELECT * FROM bet AS b, (SELECT * FROM partecipates WHERE Uid = ?) AS p WHERE b.Bid = p.Bid;", [
            user_id]

    elif status == 'won':
        query = "SELECT * FROM bet AS b, (SELECT Bid FROM win WHERE Uid = ?) AS w WHERE b.Bid = w.Bid;", [
            user_id]

    elif status == 'lost':
        query = "SELECT * FROM bet AS b, (SELECT Bid FROM partecipates WHERE Uid=? AND Uid NOT IN (SELECT Uid FROM win WHERE Uid=?)) AS p WHERE b.status='closed'", [
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
    Uid = request.json['Uid']
    invited_Uid = request.json['invited_Uid']
    bet = dict(request.json['bet'])
    db = get_db()

    try:
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO bet (title, description, ticket, pool) VALUES (?, ?, ?, ?)', [
                bet.get('title', bet.get('description'), bet.get('ticket'), bet.get('ticket'))]
        )
        db.commit()
        Bid = cursor.lastrowid

    except Exception as e:
        print(e)
        return e, 500

    try:
        db.execute(
            'INSER INTO invite (Bid, Uid, invited_Uid) VALUES (?, ?, ?)', [
                Bid, Uid, invited_Uid]
        )
        db.commit()
    except Exception as e:
        print(e)
        return e, 500

    return 'Ok', 200
