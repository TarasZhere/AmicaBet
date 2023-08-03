from flask import Blueprint, redirect, session, url_for, request, flash, abort
from amica.auth import login_required
from amica.db import get_db
bp = Blueprint('bet', __name__, url_prefix='/bet')


@bp.route('create/', methods=['POST'])
@login_required
def create():
    bet = dict(
        Uid=session.get('Uid'),
        title=request.form['title'],
        description=request.form['description'],
        ticket=int(request.form['ticket']),
        invited_Uid=request.form['invited_Uid']
    )
    db = get_db()

    # Get ticket balance from user
    balance = db.execute('SELECT balance FROM user WHERE Uid=?', [
                         session.get('Uid')]).fetchone()
    balance = dict(balance).get('balance')

    if bet.get('ticket') > balance:
        # add category

        flash('Insufficient balance', category='warning')
        return redirect(url_for('user.homepage'))

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

        # send notification to invited user
        user_name = db.execute(
            "SELECT fname, lname FROM user WHERE Uid=?", [session.get('Uid')]).fetchone()

        user_name = dict(user_name)

        db.execute(
            "INSERT INTO notification (Uid, message) VALUES (?, ?)", [
                bet.get(
                    'invited_Uid'), f'You have been invited to a bet by {user_name["fname"]} {user_name["lname"]}.'
            ])

        db.commit()
    except Exception as e:
        print(e)
        return e, 500

    return redirect(url_for('user.homepage'))


@bp.route('accept')
@bp.route('accept/<int:Bid>')
@login_required
def accept(Bid):
    db = get_db()

    # Get ticket balance from user
    user = db.execute('SELECT balance, fname, lname FROM user WHERE Uid=?', [
        session.get('Uid')]).fetchone()

    user = dict(user)
    balance = user.get('balance')

    # get bet
    bet = db.execute('SELECT * FROM bet WHERE Bid=?', [Bid]).fetchone()
    bet = dict(bet)

    # flash insufficient balance
    if bet.get('ticket') > balance:
        flash('Insufficient balance. You can\'t accept the bet', category='warning')
        return ('OK', 200)

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

        # get the invited user
        notifiedUid = db.execute(
            'SELECT Uid FROM invite WHERE Bid = ?', [Bid])

        notifiedUid = dict(notifiedUid.fetchone()).get('Uid')

        db.execute(
            "INSERT INTO notification (Uid, message) VALUES (?, ?)", [
                notifiedUid, f'Your bet with {user["fname"]} {user["lname"]} has been accepted.'
            ])

        db.commit()
    except Exception as e:
        print(e)
        return e, 500

    return ('OK', 200)


# get winner for bid
@bp.route('winner/<int:Bid>')
@login_required
def winner(Bid):
    db = get_db()

    winner = db.execute(
        'SELECT * FROM win WHERE Bid = ?', [Bid]).fetchone()

    if winner is None:
        return 'This bet is faulty. No winner.', 200

    winner = dict(winner)
    msg = "You lost!"

    if winner.get('Uid') == session.get('Uid'):
        msg = 'You won!'

    return msg, 200


@bp.route('reject')
@bp.route('reject/<int:Bid>')
@login_required
def reject(Bid):
    db = get_db()
    try:
        # update the status of the invite
        db.execute(
            'UPDATE invite SET status = "rejected" WHERE Bid = ? and invited_Uid = ?', [Bid, session.get('Uid')])
        db.execute(
            'UPDATE bet SET status = "rejected" WHERE Bid = ?', [Bid])
        db.commit()
    except Exception as e:
        print(e)
        return e, 500

    Uid = db.execute(
        "SELECT Uid FROM invite WHERE Bid= ?", [Bid]).fetchone()

    Uid = dict(Uid).get('Uid')

    fname = db.execute(
        "SELECT fname FROM user WHERE Uid=?", [session.get('Uid')]).fetchone()

    fname = dict(fname).get('fname').capitalize()

    try:
        db.execute(
            "INSERT INTO notification (Uid, message) VALUES (?, ?)", [Uid, f'{fname} rejected your bet.'])
        db.commit()
    except Exception as e:
        print('Could not notify users')
        print(e)
        return

    return ('OK', 200)

# get bet


@bp.route('/get_bet/<int:Bid>')
@login_required
def get_bet(Bid):
    db = get_db()

    bet = db.execute('SELECT * FROM bet WHERE Bid=?', [Bid]).fetchone()

    if bet is None:
        return None, 404

    # get inviteduser
    invited = db.execute('''
    SELECT * 
    FROM user as u, invite as i
    WHERE u.Uid = i.invited_Uid
    AND i.Bid = ?
    ''', [Bid]).fetchone()

    invited = dict(invited)

    # get inviteduser
    creator = db.execute('''
    SELECT * 
    FROM user as u, invite as i
    WHERE u.Uid = i.Uid
    AND i.Bid = ?
    ''', [Bid]).fetchone()

    creator = dict(creator)

    bet = dict(bet)

    return {'bet': bet, 'invited': invited, 'creator': creator}, 200
