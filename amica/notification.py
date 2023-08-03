from flask import Blueprint, jsonify, flash, redirect, render_template, session, url_for, request, abort
from amica.auth import login_required
from amica.db import get_db

###############################
# User notification apis      #
# Blue print of user          #
###############################

bp = Blueprint('notification', __name__, url_prefix='/notification')


@bp.route('get/')
@login_required
def get():
    db = get_db()
    try:
        notifications = db.execute(
            'SELECT * FROM notification WHERE Uid = ? and viewed = FALSE', [session.get('Uid')]).fetchall()

        notifications = list(map(lambda i: dict(i), notifications))

        for n in notifications:
            db.execute('UPDATE notification SET viewed = TRUE WHERE Nid = ?', [
                n.get('Nid')])
        db.commit()

    except Exception as e:
        print(e)
        abort(500)

    return notifications, 200
