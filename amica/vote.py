from flask import Blueprint, session, jsonify, request
from requests import post, get, HTTPError
from amica.server_url import SERVER_URL as URL, headers as h
from amica.auth import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/', methods=['POST'])
def vote():
    voted = {
        'Uid': session.get('Uid'),
        'Bid': request.json['Bid'],
        'voted_Uid': request.json['voted_Uid']
    }

    try:
        response = post(URL+'vote/', headers=h, json=voted)

        if response.status_code == 409:
            return "You already voted!", 409

        response.raise_for_status()

    except Exception as e:
        print(e)
        return e, 500

    return 'Ok', 200
