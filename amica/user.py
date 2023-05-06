from flask import (
    Blueprint, redirect, render_template, session, url_for
)
from requests import post
from amica.auth import login_required
from amica.server_url import SERVER_URL as URL, headers


###############################
# User hompage related apis   #
# Blue print of user          #
###############################

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('homepage')
@login_required
def homepage():
    user_id = session.get('Uid')

    try:
        response = post(URL+'user/uid', json={'Uid':user_id}, headers=headers)
        user = response.json()
    except:
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Getting user friends list so it can be displayed
    try:
        response = post(URL+'user/friends', json={'Uid':user_id}, headers=headers)
        if response.status_code == 404:
            print('Error in "user/profile": No friends found ...')
            friends = []
        else: 
            friends = response.json()
    except:
        session.clear()
        return redirect(url_for('auth.login'))


    return render_template('user/homepage.html', user=user, friends = friends)


@bp.route('profile')
@login_required
def profile():
    user_id = session.get('Uid')

    # Getting user information
    try:
        response = post(URL+'user/uid', json={'Uid':user_id}, headers=headers)
        user = response.json()
    except:
        session.clear()
        return redirect(url_for('auth.login'))
    

    
    
    return render_template('user/profile.html', user=user)