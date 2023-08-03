from flask import Blueprint, session, request, flash, abort
from amica.auth import login_required
from amica.db import get_db
from amica.logic import bet_logic_valid


bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/', methods=['POST'])
@login_required
def vote():
    voted_Uid = request.json['voted_Uid']
    Bid = request.json['Bid']
    Uid = session.get('Uid')
    db = get_db()

    # add new vote if user has not voted
    try:
        db.execute('INSERT INTO vote (Bid, Uid, voted_Uid) values (?,?,?)', [
            Bid, Uid, voted_Uid])
        db.commit()
    except Exception as e:
        print(e)
        flash('You already voted!', category='warning')
        return e, 500

    updateBetStatus(Bid)

    return 'ok', 200


def updateBetStatus(Bid):
    db = get_db()
    # check if both users have voted
    all_votes = db.execute(
        'SELECT * FROM vote WHERE Bid = ?', [Bid]).fetchall()

    all_votes = [dict(vote) for vote in all_votes]
    print("All votes:", all_votes)

    if len(all_votes) < 2:
        print('Not enough votes')
        return

    winner_Uid = bet_logic_valid(all_votes)

    print('winner', winner_Uid)

    if not winner_Uid:
        # Giving back a part of the monney
        ticket = db.execute(
            'SELECT ticket FROM bet WHERE Bid = ?', [Bid]).fetchone()
        ticket = dict(ticket).get('ticket') * 0.9

        try:
            Uids = db.execute(
                "SELECT Uid, invited_Uid FROM invite WHERE Bid = ?", [Bid]).fetchone()
            Uids = dict(Uids)

            for Uid in Uids.values():
                db.execute(
                    f"""
                    UPDATE user
                    SET balance = balance + FLOOR({ticket})
                    WHERE Uid = {Uid};
                    """
                )
            db.commit()
        except Exception as e:
            print('Could not update balance')
            print(e)
            return
    else:
        ticket = db.execute(
            f'SELECT ticket FROM bet WHERE Bid={Bid}').fetchone()
        pool = dict(ticket).get('ticket') * 2

        try:
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
            db.commit()
        except Exception as e:
            print('Could not update balance on winner')
            print(e)
            return

    # closing the bet
    try:
        db.execute(f'UPDATE bet SET status="closed" WHERE Bid={Bid}')
        db.commit()
    except Exception as e:
        print('Could not close bet')
        print(e)
        return

    # notify users that one of the bets has been closed
    Uids = db.execute(
        "SELECT Uid, invited_Uid FROM invite WHERE Bid= ?", [Bid]).fetchone()
    Uids = dict(Uids)

    print('Uids', Uids)

    try:
        for Uid in Uids.values():
            db.execute(
                "INSERT INTO notification (Uid, message) VALUES (?, ?)", [Uid, 'One of your bets has been closed!'])
        db.commit()
    except Exception as e:
        print('Could not notify users')
        print(e)
        return


@bp.route('/<int:Bid>', methods=['GET'])
@login_required
def get(Bid):
    db = get_db()
    vote = db.execute(
        'SELECT voted_Uid FROM vote WHERE Bid = ? and Uid = ?', [Bid, session.get('Uid')]).fetchone()

    if not vote:
        return abort(404)
    print('Vote', dict(vote))

    voted_Uid = dict(vote).get('voted_Uid')
    if voted_Uid == session.get('Uid'):
        return "You voted for yourself", 200
    else:
        return "You voted for the opponent", 200
