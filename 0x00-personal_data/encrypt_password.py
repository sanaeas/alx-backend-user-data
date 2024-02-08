#!/usr/bin/env python3
"""Module to encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashe the given password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate the provided password against the hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
