from flask import Blueprint, session, abort, request
from requests import post, HTTPError, get
from amica.server_url import SERVER_URL as URL, headers as h
from amica.auth import login_required

bp = Blueprint('friend', __name__, url_prefix='/friend')


@bp.route('add/<int:receiver_Uid>')
@login_required
def add(receiver_Uid):

    sender_Uid = session.get('Uid')
    try:
        response = post(url=URL+'friend/add', headers=h, json={
            'Uid': sender_Uid,
            'receiver_Uid': receiver_Uid
        })

        response.raise_for_status()

    except HTTPError as e:
        print(e)
        abort(500)

    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200

@bp.route('get/<int:friend_Uid>')
@login_required
def get_friend(friend_Uid):
    try:
        response = get(f'{URL}friend/{friend_Uid}/{session.get("Uid")}')
        response.raise_for_status()
    except HTTPError as e:
        print(e)
        return abort(500)
    except Exception as e:
        print(e)
        return abort(500)

    user = response.json()
    return user, 200


@bp.route('accept', methods=['POST'])
@login_required
def accept():
    sender_Uid = request.json['sender_Uid']
    receiver_Uid = session.get('Uid')
    try:
        response = post(URL+'friend/accept', headers=h,
                        json={'sender_Uid': sender_Uid, 'receiver_Uid': receiver_Uid})

        response.raise_for_status()

    except HTTPError as e:
        print(e)
        abort(500)
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200


@bp.route('reject', methods=['POST'])
@login_required
def reject():
    sender_Uid = request.json['sender_Uid']
    receiver_Uid = session.get('Uid')
    try:
        response = post(URL+'friend/reject', headers=h,
                        json={'sender_Uid': sender_Uid, 'receiver_Uid': receiver_Uid})

        response.raise_for_status()

    except HTTPError as e:
        print(e)
        abort(500)
    except Exception as e:
        print(e)
        abort(500)

    return 'Ok', 200
