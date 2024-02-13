#!/usr/bin/env python3
""" Module to manage the API authentication
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ A class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Method to get authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get current user
        """
        return None
