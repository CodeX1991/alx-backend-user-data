#!/usr/bin/env python3
"""Auth class"""


from flask import request
from typing import List, TypeVar
import os


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
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the Flask request object

        Args:
            request: The request field default None
        Returns:
            None
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the Flask request objects

        Args:
            request: The request field default None
        Returns:
            None
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie vale from a request"""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(session_name)
