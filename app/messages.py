from flask import (
    Blueprint, request, g, request, jsonify
)

from .db import get_db
from .queries import (
    get_user_by_name, send_message, get_messages, delete_message,
    get_unread_messages, read_message, get_received_message, 
    get_sent_message
)
from .validators import login_required

bp = Blueprint('messages', __name__, url_prefix='/messages')


@bp.route('', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    
    if request.method == 'POST':  # send a message
        # validate form input
        required = ('To', 'Subject', 'Message')
        missing = [key for key in required if key not in request.form]

        if len(missing) > 0:
            return f'Missing form keys: {", ".join(missing)}.', 400

        # send the message
        receiver = get_user_by_name(request.form['To'], db)
        
        if receiver is None:
            return 'The requested receiver does not exist.', 404
        
        message = {
            'sender_id': g.user['id'],
            'receiver_id': receiver['id'],
            'subject': request.form['Subject'],
            'message': request.form['Message']
        }

        # store message in db and return Created upon success
        send_message(message, db)
        return 'Message sent.', 201

    # method == GET: return received messages
    return jsonify(get_messages(g.user['id'], db))


@bp.route('/unread')
@login_required
def unread():
    db = get_db()
    
    # return unread messages
    return jsonify(get_unread_messages(g.user['id'], db))


@bp.route('/<int:message_id>', methods=['GET', 'DELETE'])
@login_required
def specific_message(message_id: int):
    db = get_db()
    
    # validate message_id
    received_msg = get_received_message(g.user['id'], message_id, db)
    sent_msg = get_sent_message(g.user['id'], message_id, db)
    
    if received_msg is None and sent_msg is None:
            return 'Requested message does not exist.', 404
    
    if request.method == 'DELETE':
        delete_message(g.user['id'], message_id, db)
        return 'Message deleted successfully.'
    
    # method == GET: if connected user sent the message
    if received_msg is None:
        return sent_msg
    
    # if connected user received the message, update the db it is read
    read_message(message_id, db)
    return received_msg
