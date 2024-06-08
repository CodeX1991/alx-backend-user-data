#!/usr/bin/env python3
"""Session expiration authentication Class"""


from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Session expiration authentication class"""
    def __init__(self):
        """Initialization"""
        super().__init__()
        session_duration = os.getenv('SESSION_DURATION')

        try:
            self.session_duration = int(session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session ID and set the session dictionary with expiration

        Args:
            user_id (str): The user id for the session
        Returns:
            The session id created
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dict = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the user ID based on session ID with expiration check"""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        if "created_at" not in session_dict:
            return None

        created_at = session_dict["created_at"]

        if created_at + timedelta(seconds=self.session_duration) \
                < datetime.now():
            return None

        return session_dict.get("user_id")
