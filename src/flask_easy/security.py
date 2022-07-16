"""
authentication.py

Author: Joseph Maclean Arhin
"""

import typing as t
import inspect
from dataclasses import dataclass, field
from functools import cached_property, wraps
from flask import request, Request

from flask_easy.exc import Unauthorized


@dataclass
class UserDetailsToken:
    """
    Contains the summary of the user i.e username and the roles the user can perform
    """

    username: str = field(default_factory=str)
    roles: t.List[str] = field(default_factory=list)


class TokenDecoder:
    """
    To be inherited
    """

    request: Request

    def decode_token(self) -> UserDetailsToken:
        """This method is called for every request.
        It should contain the logic for decoding tokens/authenticating users"""
        raise NotImplementedError

    @classmethod
    def set_request(cls, request_obj):
        """request is loaded at runtime into the class context"""
        cls.request = request_obj


class Auth:
    """Main auth class"""

    token_decoder: t.Type[TokenDecoder]
    user_details: UserDetailsToken

    @cached_property
    def user_name(self):
        """Return username"""
        return self.user_details.username

    @cached_property
    def get_roles(self):
        """Return roles"""
        return self.user_details.roles

    def register_token_decoder(self, token_decoder: t.Type[TokenDecoder]):
        """Register token decoder"""
        self.token_decoder = token_decoder

    def __call__(self, *args, **kwargs):
        if not self.token_decoder:
            return
        self.user_details = self.token_decoder().decode_token()


def auth_required(roles=None):
    """auth required decorator"""

    def authorize_user(func):
        """
        A wrapper to authorize an action using
        :param func: {function}` the function to wrap around
        :return:
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            # Append service name to function name to form role

            authenticator.token_decoder.set_request(request)
            authenticator()
            user_roles = authenticator.get_roles
            if is_authorized(user_roles, roles or []):
                if "username" in inspect.getfullargspec(func).args:
                    kwargs["username"] = authenticator.user_name
                return func(*args, **kwargs)

            raise Unauthorized()

        return view_wrapper

    return authorize_user


def is_authorized(user_roles, required_roles):
    """Check if access roles is in available roles"""

    for role in required_roles:
        if role not in user_roles:
            return False

    return True


authenticator = Auth()
