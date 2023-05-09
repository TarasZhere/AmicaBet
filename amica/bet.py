from flask import Blueprint, session, abort, request
from requests import post, HTTPError
from amica.server_url import SERVER_URL as URL, headers as h
from amica.auth import login_required

bp = Blueprint('bet', __name__, url_prefix='/bet')


@bp.route('create', methods=['POST'])
@login_required
def create():
    bet = dict(request.json)
    print(bet)

    return "OK", 200
