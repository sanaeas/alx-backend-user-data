#!/usr/bin/env python3
""" Module to manage the API authentication
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ Extract the Base64 part of the Authorization header
        """
        if (authorization_header is None or
           not isinstance(authorization_header, str) or
           not authorization_header.startswith("Basic ")):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Method to decode a Base64 string
        """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user credentials
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ Retrieve the User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            user_list = User.search({'email': user_email})
        except KeyError:
            return None
        if not user_list or not user_list[0].is_valid_password(user_pwd):
            return None
        return user_list[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieve the User instance for a request
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(
            authorization_header)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        email, password = self.extract_user_credentials(decoded_header)
        if email is None or password is None:
            return None

        return self.user_object_from_credentials(email, password)
