#!/usr/bin/env python3
"""
Basic auth
"""


from .auth import Auth
import base64


class BasicAuth(Auth):
    """
    A Basic auth class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        Extract base64 authorization header

        Args:
            authorization_header (str): the auth header
        Returns:
            The base64 of the Authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Decodes the Base64 part of the Authorization header

        Args:
            base64_authorization_header (str): Base64 auth header
        Returns:
            the value as UTF8 string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Extracts the user credentials from the decoded Base64 string

        Args:
            decoded_base64_authorization_header (str): decoded base64 auth_h
        Returns:
            the user email and the user password
            -these 2 values must be separated by a :
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1])
