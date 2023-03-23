from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from amica.db import get_db
from amica.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('homepage', methods=['GET'])
@login_required
def homepage():
    uid = session.get('user_id')
    db = get_db()
    if uid:
        user = db.execute(
            f'SELECT * FROM user WHERE id = {uid}'
        ).fetchone()
        return render_template('user/homepage.html', user=user)

    redirect(url_for('landing'))

@bp.route('profile', methods=['GET', 'POST'])
@login_required
def profile():
    id = session.get('user_id')
    user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (id,)
    ).fetchone()

    if not user:
        redirect(url_for('auth.login'))


    
    return render_template('user/profile.html', user=user)