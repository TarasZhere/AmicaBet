from flask import Blueprint, flash, redirect, render_template, session, url_for, request, abort
from amica.auth import login_required
from amica.db import get_db

###############################
# User hompage related apis   #
# Blue print of user          #
###############################

# Helpers functions


def get_all_friends():
    db = get_db()

    def checkStatus(rec_friend):
        friend = dict(rec_friend)
        if friend.get('status') == 'pending':
            friend['status'] = 'request'
        return friend

    received = db.execute(
        'SELECT Uid, fname, lname, email, status, balance balance FROM (SELECT * FROM friendRequest WHERE receiver_Uid = ? AND (status != "blocked" AND status != "rejected")) AS friends, user AS u WHERE friends.sender_Uid = u.Uid', [
            session.get('Uid')]
    ).fetchall()
    friends = list(map(lambda i: checkStatus(i), received))
    requested = db.execute(
        'SELECT Uid, fname, lname, email, status, balance FROM (SELECT * FROM friendRequest WHERE sender_Uid = ? AND (status != "blocked" AND status != "rejected")) AS friends, user AS u WHERE friends.receiver_uid = u.Uid', [
            session.get('Uid')]
    ).fetchall()

    list(map(lambda i: friends.append(dict(i)), requested))

    return friends


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('homepage/')
@bp.route('homepage/<string:status>')
@login_required
def homepage(status=None):

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

    try:
        friends = get_all_friends()
    except Exception as e:
        print(e)
        friends = None

    user_id = session.get('Uid')
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
        query = "SELECT * FROM bet AS b, invite as i, win AS w WHERE w.Uid = ? AND b.Bid = w.Bid AND i.Bid = b.Bid", [
            user_id]

    elif status == 'lost':
        query = "SELECT * FROM bet AS b, (SELECT * FROM invite WHERE Uid = ? OR invited_Uid = ?) AS i WHERE b.Bid = i.Bid AND b.status='closed' AND b.Bid NOT IN (SELECT b.Bid FROM bet AS b, invite as i, win AS w WHERE w.Uid = ? AND b.Bid = w.Bid AND i.Bid = b.Bid)", [
            user_id, user_id, user_id]

    try:
        db = get_db()
        bets = db.execute(*query).fetchall()

    except Exception as e:
        bets = None
        print(e)
    else:
        bets = list(map(lambda i: dict(i), bets))

    return render_template('user/homepage2.html', user=user, friends=friends, bets=bets)


@bp.route('profile')
@login_required
def profile():
    db = get_db()
    # Getting user information
    try:
        user = db.execute('SELECT * FROM user WHERE Uid = ?',
                          (session.get('Uid'),)).fetchone()
        if user is None:
            Exception('User not found')
        else:
            user = dict(user)

        info = db.execute('SELECT * FROM profileInfo WHERE Uid = ?',
                          (session.get('Uid'),)).fetchone()

        if info is None:
            flash('Please complete your profile', 'warning')
        else:
            info = dict(info)

    except Exception as e:
        print(e)
        session.clear()
        return redirect(url_for('auth.login'))

    try:
        friends = get_all_friends()
    except Exception as e:
        print(e)
        friends = None

    return render_template('user/profile.html', user=user, info=info, friends=friends)


@bp.route('search', methods=['GET', 'POST'])
@login_required
def search():
    db = get_db()
    if request.method == 'GET':
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
        return render_template('user/search.html', user=user)

    input_search = request.json['input_search'].lower()
    cursor = db.cursor()
    try:
        Uid = session.get('Uid')
        query = f"SELECT Uid, fname, lname, email FROM user WHERE (fname LIKE ? OR lname LIKE ?) AND Uid NOT IN (SELECT sender_Uid FROM friendRequest WHERE sender_Uid={Uid} OR receiver_Uid={Uid}) AND Uid NOT IN (SELECT receiver_Uid FROM friendRequest WHERE sender_Uid={Uid} OR receiver_Uid={Uid})"

        cursor.execute(query, ('%' + input_search +
                       '%', '%' + input_search + '%'))
        users = cursor.fetchall()
        cursor.close()

    except Exception as e:
        print(e)
        abort(500)
    else:
        users = list(map(lambda i: dict(i), users))

    return render_template('/user/macros/user.macro.html', users=users)


@bp.route('completeProfile', methods=['POST'])
@login_required
def completeProfile():

    phone_number = request.form['phone_number']
    address = request.form['address']
    state = request.form['state']
    city = request.form['city']

    db = get_db()
    try:
        db.execute(
            'INSERT INTO profileInfo (Uid, phone_number, address, state, city) VALUES (?, ?, ?, ?, ?)',
            [session.get('Uid'), phone_number, address, state, city])
        db.commit()
    except Exception as e:
        print(e)
        flash('Something went wrong', 'danger')
        return redirect(url_for('user.profile'))

    flash('Profile updated successfully', 'success')
    return redirect(url_for('user.profile'))


@bp.route('editProfile', methods=['POST'])
@login_required
def editProfile():

    address = request.form['address']
    state = request.form['state']
    city = request.form['city']

    db = get_db()
    try:
        # update profile info
        db.execute(
            'UPDATE profileInfo SET address=?, state=?, city=? WHERE Uid=?',
            [address, state, city, session.get('Uid')])
        db.commit()
    except Exception as e:
        print(e)
        flash('Something went wrong', 'danger')
        return redirect(url_for('user.profile'))

    flash('Profile updated successfully', 'success')
    return redirect(url_for('user.profile'))


# add balance
@bp.route('addBalance', methods=['GET'])
@login_required
def addBalance():
    # db = get_db()
    # try:
    #     db.execute('UPDATE user SET balance=balance+? WHERE Uid=?',
    #                [20, session.get('Uid')])
    #     db.commit()
    # except Exception as e:
    #     print(e)
    #     flash('Something went wrong', 'danger')

    # else:
    #     flash('Balance added successfully', 'success')

    flash('Currently, it is not possible to add balance. Every month each user will receive 20 tokens.', 'warning')

    return redirect(url_for('user.homepage'))
