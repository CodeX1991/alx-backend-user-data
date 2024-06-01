#!/usr/bin/env python3
"""Encrypting passwords"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrpt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        bytes: the salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password
        password (str): The plain-text password.
    Returns:
        bool: True if the password matches the hased password,
              Fale otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
