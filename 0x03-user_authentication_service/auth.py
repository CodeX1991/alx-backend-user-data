#!/usr/bin/env python3
"""Handling password authwntication"""


import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Authenticat user

        Args:
            email (str): the email of the user
            password (str): password of the user
        Returns:
            the user object
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validation"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                hashed_password = user.hashed_password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return True

        except NoResultFound:
            return False

        return False


def _hash_password(password: str) -> bytes:
    """
    Hash the password

    Args:
        password (str): the password t be hash
    Returns:
        The bytes correspondence
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
