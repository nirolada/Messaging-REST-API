from flask import (
    Blueprint, g, request, session
)
from werkzeug.security import check_password_hash

from .db import get_db
from .queries import create_user, get_user_by_name, get_user
from .validators import login_required, already_logged_in

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
@already_logged_in
def register():
    # validate form input
    required = ('Username', 'Password')
    missing = [key for key in required if key not in request.form]

    if len(missing) > 0:
        return f'Missing form keys: {", ".join(missing)}.', 400
    
    # check for user existence in the db
    username, password = request.form['Username'], request.form['Password']
    db = get_db()
    if get_user_by_name(username, db) is not None:
        return f'"{username}" is already registered.', 400

    # store input user in the db
    create_user(username, password, db)
    return 'User created successfully.', 201


@bp.route('/login', methods=['POST'])
@already_logged_in
def login():
    # validate form input
    required = ('Username', 'Password')
    missing = [key for key in required if key not in request.form]

    if len(missing) > 0:
        return f'Missing form keys: {", ".join(missing)}.', 400
    
    # handle request
    username, password = request.form['Username'], request.form['Password']
    db = get_db()
    user = get_user_by_name(username, db)

    # validate username and password
    if user is None:
        return 'Incorrect username.', 400
    elif not check_password_hash(user['password'], password):
        return 'Incorrect password.', 400

    # store user_id in session upon success
    session.clear()
    session['user_id'] = user['id']
    return 'Logged in successfully.'


@bp.before_app_request
def load_logged_in_user():
    # load logged in user before handling a request
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_user(user_id, get_db())


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return 'Logged out successfully.'