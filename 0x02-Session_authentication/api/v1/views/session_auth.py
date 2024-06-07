#!/usr/bin/env python3
"""Handles all routes for the Session Authentication"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False
        )
def login():
    """POST /auth_session/login

    Returns:
        - User object JSON representation
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email == "" or email is None:
        return jsonify({"error": "email missing"}), 400

    if password == "" or password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    user_json = user.to_json()

    response = jsonify(user_json)
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
