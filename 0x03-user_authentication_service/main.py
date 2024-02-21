#!/usr/bin/env python3
""" End-to-end integration test
"""
import requests

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """ Test register user
    """
    url = f"{BASE_URL}/users"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test login with wrong password
    """
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 401


def profile_unlogged() -> None:
    """ Test going to /profile without being logged in
    """
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """ Test login
    """
    url = f"{BASE_URL}/sessions"
    response = requests.post(url, data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """ Test going to profile while being logged in
    """
    url = f"{BASE_URL}/profile"
    response = requests.get(url, cookies={"session_id": session_id})
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """ Test logout
    """
    url = f"{BASE_URL}/sessions"
    response = requests.delete(url, cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """ Test reset password token
    """
    url = f"{BASE_URL}/reset_password"
    response = requests.put(url, data={"email": email})
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test update password
    """
    url = f"{BASE_URL}/reset_password"
    response = requests.put(url, data={"email": email,
                                       "reset_token": reset_token,
                                       "new_password": new_password})
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
