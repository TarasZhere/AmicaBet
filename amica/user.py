from flask import Blueprint, flash, redirect, render_template, session, url_for, request, abort
from requests import post
from amica.auth import login_required
from amica.server_url import SERVER_URL as URL, headers
from requests.exceptions import HTTPError

###############################
# User hompage related apis   #
# Blue print of user          #
###############################

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('homepage/')
@bp.route('homepage/<string:status>')
@login_required
def homepage(status=None):
    user_id = session.get('Uid')

    try:
        response = post(URL+'user/uid', json={'Uid': user_id}, headers=headers)
        user = response.json()
    except:
        session.clear()
        return redirect(url_for('auth.login'))

    # Getting user friends list so it can be displayed
    try:
        response = post(URL+'user/friends',
                        json={'Uid': user_id}, headers=headers)
        if response.status_code == 404:
            print('Error in "user/profile": No friends found ...')
            friends = []
        else:
            friends = response.json()
    except:
        session.clear()
        return redirect(url_for('auth.login'))

    # get all bets!
    try:
        response = post(URL+'bet/', json={
            'Uid': user_id, 'status': status
        }, headers=headers)

        if response.status_code == 500:
            bets = None
        else:
            bets = response.json()

    except Exception as e:
        bets = None
        print(e)

    return render_template('user/homepage.html', user=user, friends=friends, bets=bets)


@bp.route('profile')
@login_required
def profile():
    user_id = session.get('Uid')

    # Getting user information
    try:
        response = post(URL+'user/uid', json={'Uid': user_id}, headers=headers)
        user = response.json()
    except:
        session.clear()
        return redirect(url_for('auth.login'))

    return render_template('user/profile.html', user=user)


@bp.route('search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'GET':
        return render_template('user/search.html')

    input_search = request.json['input_search']
    try:
        response = post(
            URL+f'friend/search/{input_search}', json={'Uid': session.get('Uid')}, headers=headers)
        response.raise_for_status()

    except HTTPError as exc:
        print(exc)
        flash('Http error')

    except Exception as e:
        print(e)
        abort(500)

    users = response.json()

    return render_template('/user/macros/user.macro.html', users=users)
