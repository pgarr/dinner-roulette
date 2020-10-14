from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity

from app.api.errors import error_response
from app.api_auth import bp
from app.api_auth.helpers import get_fresh_jwt_token, is_email_unique, is_username_unique


@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    payload = get_fresh_jwt_token(username, password, with_refresh_token=True)
    if payload:
        return jsonify(payload), 200
    else:
        return error_response(401, "Bad username or password")


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    username = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=username, fresh=False)
    }
    return jsonify(ret), 200


@bp.route('/fresh-login', methods=['POST'])
def fresh_login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    payload = get_fresh_jwt_token(username, password, with_refresh_token=False)
    if payload:
        return jsonify(payload), 200
    else:
        return error_response(401, "Bad username or password")


@bp.route('/validate', methods=['GET'])
def validate():
    email = request.args.get('email', None)
    username = request.args.get('username', None)
    payload = {}
    if email:
        payload['email'] = {'unique': is_email_unique(email)}
    if username:
        payload['username'] = {'unique': is_username_unique(username)}
    return jsonify(payload), 200


@bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    email = request.json.get('email', '')
