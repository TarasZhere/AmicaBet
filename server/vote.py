from flask import Blueprint, request, abort
from server.db import get_db

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/', methods=['POST'])
def vote():
    Uid = request.json['Uid']
    voted_Uid = request.json['voted_Uid']
    Bid = request.json['Bid']

    db = get_db()

    try:

        voted = db.execute(
            f'''
            SELECT * FROM vote WHERE Bid = {Bid} AND Uid = {Uid}
            '''
        ).fetchall()

        if voted:
            return 'Conflict', 409

        db.execute(
            f'''
            INSERT INTO vote (Bid, Uid, voted_Uid) VALUES (?, ?, ?)
            ''',
            [Bid, Uid, voted_Uid]
        )

        db.commit()

    except Exception as e:
        print(e)
        return e, 500

    return 'Ok', 200


@bp.route('/all')
def all():
    votes = get_db().execute('SELECT * FROM vote;')

    for vote in votes:
        print(dict(vote))

    return 'ok', 200
