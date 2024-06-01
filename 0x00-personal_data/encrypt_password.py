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
