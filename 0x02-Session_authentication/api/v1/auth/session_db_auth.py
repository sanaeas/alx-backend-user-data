#!/usr/bin/env python3
""" Module to manage the API authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session authentication with database storage
    """

    def create_session(self, user_id=None) -> str:
        """ Create a Session ID for a user
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Retrieve User ID based on Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if not user_sessions or len(user_sessions) <= 0:
            return None

        user_session = user_sessions[0]
        return super().user_id_for_session_id(user_session.session_id)

    def destroy_session(self, request=None) -> bool:
        """ Destroy UserSession based on Session ID
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if not user_sessions or len(user_sessions) <= 0:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return super().destroy_session(request)
