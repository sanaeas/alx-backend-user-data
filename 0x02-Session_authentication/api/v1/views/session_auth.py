#!/usr/bin/env python3
""" Handle all routes for the Session authentication
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
from os import environ


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Handle user login and session creation
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users_list = User.search({"email": email})
        assert (type(users_list) == list) and (len(users_list) == 1)
    except (KeyError, AssertionError):
        return jsonify({"error": "no user found for this email"}), 404
    user = users_list[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(environ.get("SESSION_NAME", "set_cookie"), session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ Handle user logout and session destruction
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
