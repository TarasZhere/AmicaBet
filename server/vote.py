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
            'SELECT * FROM vote WHERE Bid = ? AND Uid = ?', [Bid, Uid]).fetchall()

        # if user has not voted insert a new vote
        if not voted:
            db.execute('INSERT INTO vote (Bid, Uid, voted_Uid) values (?,?,?)', [
                       Bid, Uid, voted_Uid])
            db.commit()
            return 'ok', 200

        all_votes = db.execute(
            'SELECT * FROM vote WHERE Bid = ?', [Bid]).fetchall()
        # if both user have voted update
        if len(all_votes) > 1:
            from server.logic import bet_logic_valid
            winner_Uid = bet_logic_valid(all_votes)

            if not winner_Uid:
                # Giving back a part of the monney
                db.execute(
                    f"""
                    UPDATE user
                    SET balance = balance + FLOOR(i.ticket * 0.9)
                    FROM (
                        SELECT Uid, invite_Uid
                        FROM invite
                        WHERE Bid = {Bid}
                    ) as i
                    WHERE Uid = i.Uid OR Uid = i.invite_Uid
                    """
                )

            # if we have a winner
            else:
                ticket = db.execute(
                    f'SELECT ticket FROM bet WHERE Bid={Bid}').fetchone()
                pool = dict(ticket).get('ticket') * 2

                db.execute(
                    f'''
                    UPDATE user
                    SET balance = balance + {pool}
                    WHERE Uid={winner_Uid}
                    '''
                )
                # Update winner table
                db.execute(f'INSERT INTO win (Bid, Uid) VALUES (?, ?)', [
                           Bid, winner_Uid])

            # closing the bet
            db.execute(f'UPDATE bet SET status="closed" WHERE Bid={Bid}')
            db.commit()
            return 'ok', 200

        # You already voted therefore just wait!!
        return "You already voted!", 409

    except Exception as e:
        print(e)
        return e, 500


@bp.route('all')
def all():
    v = get_db().execute('SELECT * FROM vote')

    list(map(lambda i: print(dict(i)), v))

    return 'ok', 200


@bp.route('win')
def win():
    v = get_db().execute('SELECT * FROM win')

    list(map(lambda i: print(dict(i)), v))

    return 'ok', 200
