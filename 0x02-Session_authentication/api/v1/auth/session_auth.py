#!/usr/bin/env python3
"""Create a session"""


from .auth import Auth
import uuid


class SessionAuth(Auth):
    """New authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a user id

        Args:
            user_id (str): the user id
        Returns:
            Session ID
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
