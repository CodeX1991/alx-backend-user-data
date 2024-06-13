#!/usr/bin/env python3
"""Handling password authwntication"""


import bcrypt


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
