#!/usr/bin/env python3
"""User session model"""


from models.base import Base


class UserSession(Base):
    """User session class"""
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a User session

        Args:
            args: Set of argument
            kwargs: varadic argument
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
