import functools
from flask import session, g


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return 'Login required.', 401

        return view(**kwargs)
    return wrapped_view


def already_logged_in(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # check if a user is already logged in, return Bad Request if so
        if session.get('user_id') is not None:
            return 'A user is already logged in.', 400

        return view(**kwargs)
    return wrapped_view
