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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip("/") + "/"
        for excluded_path in excluded_paths:
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get current user
        """
        return None
