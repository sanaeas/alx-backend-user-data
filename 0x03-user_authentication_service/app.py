#!/usr/bin/env python3
""" A basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """ Welcome route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """ Register a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
