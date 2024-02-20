#!/usr/bin/env python3
""" Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hashe a password using bcrypt
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
