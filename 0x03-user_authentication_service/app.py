#!/usr/bin/env python3
"""Basic Flask App"""


from flask import Flask, request, jsonify, abort, \
        make_response, redirect, url_for
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """An index route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Register the user if it does not exist"""
    # Get the form field
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify(
                {"email": email, "message": "user created"})
    except Exception:
        return ({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Create a session if form field exist"""
    # Get the form field
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = make_response(
            jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Delete a session"""
    # Extract the seeion id from cookies
    session_id = request.cookies.get('session_id')

    # Validate the session id
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    # Destroy the session by setting session_id to None
    AUTH.destroy_session(user.id)

    # Redirect to home page
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Get user"""
    # Extract the seeion id from cookies
    session_id = request.cookies.get('session_id')

    # Validate the session id
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
