from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity

from app.blueprints.api.errors import bad_request, error_response
from app.blueprints.api_auth import bp
from app.blueprints.api_auth.helpers import get_fresh_jwt_token
from app.blueprints.auth.email import send_password_reset_email
from app.services.auth import create_user, get_user_by_email, verify_reset_password_token, set_new_password

from app.utils.validators import validate_email, validate_username, validate_password


@bp.route('/login', methods=['POST'])
def login():
    json = request.json
    if json:
        username = json.get('username', '')
        password = json.get('password', '')
    else:
        return bad_request("Lack of required payload data")

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
    json = request.json
    if json:
        username = json.get('username', '')
        password = json.get('password', '')
    else:
        return bad_request("Lack of required payload data")

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
        is_valid, check_dict = validate_email(email)
        payload['email'] = {'valid': is_valid, 'checks': check_dict}
    if username:
        is_valid, check_dict = validate_username(username)
        payload['username'] = {'valid': is_valid, 'checks': check_dict}
    return jsonify(payload), 200


@bp.route('/register', methods=['POST'])
def register():
    json = request.json
    if json:
        username = json.get('username', '')
        password = json.get('password', '')
        email = json.get('email', '')
    else:
        return bad_request("Lack of required payload data")

    payload = {}

    is_email_valid, email_check_dict = validate_email(email)
    payload['email'] = {'valid': is_email_valid, 'checks': email_check_dict}

    is_username_valid, username_check_dict = validate_username(username)
    payload['username'] = {'valid': is_username_valid, 'checks': username_check_dict}

    is_password_valid, password_check_dict = validate_password(password)
    payload['password'] = {'valid': is_password_valid, 'checks': password_check_dict}

    if is_email_valid & is_password_valid & is_username_valid:
        create_user(username, email, password)
        status_code = 201
    else:
        status_code = 422

    return jsonify(payload), status_code


@bp.route('/reset_password', methods=['POST'])
def reset_password_request():
    json = request.json
    if json:
        email = json.get('email', '')
    else:
        return bad_request("Lack of required payload data")

    user = get_user_by_email(email)

    if user:
        send_password_reset_email(user)

    return jsonify({'message': 'Done!'}), 200


@bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    json = request.json
    if json:
        password = json.get('password', '')
    else:
        return bad_request("Lack of required payload data")

    user = verify_reset_password_token(token)
    if not user:
        return error_response(422, 'Invalid token')

    is_password_valid, password_check_dict = validate_password(password)

    if is_password_valid:
        set_new_password(user, password)
        return jsonify({'message': 'Done!'}), 200
    else:
        payload = {'password': {'valid': is_password_valid, 'checks': password_check_dict}}
        return jsonify(payload), 422
