#!/usr/bin/env python3
"""Auth class"""


from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determins if the authentication is required for a given path

        Args:
            path (str): The given path
            excluded_paths (List(str)): A list of excluded paths
        Returns:
            False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the Flask request object

        Args:
            request: The request field default None
        Returns:
            None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the Flask request objects

        Args:
            request: The request field default None
        Returns:
            None
        """
        return None
