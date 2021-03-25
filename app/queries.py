from typing import List, Any
from sqlite3 import Connection
from werkzeug.security import generate_password_hash


def create_user(username: str, password: str, db: Connection) -> None:
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()


def get_user_by_name(username: str, db: Connection) -> Any:
    return db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()


def get_user(user_id: int, db: Connection) -> Any:
    return db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


def send_message(message: dict, db: Connection) -> None:
    db.execute(
        '''
        INSERT INTO message (sender_id, receiver_id, subject, message)
        VALUES (?, ?, ?, ?)
        ''', (message['sender_id'], message['receiver_id'],
              message['subject'], message['message'])
    )
    db.commit()


def get_messages(receiver_id: int, db: Connection) -> List[Any]:
    return db.execute(
        '''
        SELECT m.id, (SELECT username FROM user WHERE id = m.sender_id) AS 'from',
            created, subject,
            (CASE unread WHEN 0 then 'Seen' WHEN 1 then 'New' END) status
        FROM message m JOIN user u
        ON m.receiver_id = u.id
        WHERE m.receiver_id = ?
        ORDER BY created DESC
        ''', (receiver_id,)
    ).fetchall()


def get_unread_messages(receiver_id: int, db: Connection) -> List[Any]:
    return db.execute(
        '''
        SELECT m.id, (SELECT username FROM user WHERE id = m.sender_id) AS 'from',
            created, subject,
            (CASE unread WHEN 0 then 'Seen' WHEN 1 then 'New' END) status
        FROM message m JOIN user u
        ON m.receiver_id = u.id
        WHERE m.receiver_id = ? AND m.unread = 1
        ORDER BY created DESC
        ''', (receiver_id,)
    ).fetchall()


def read_message(message_id: int, db: Connection) -> None:
    db.execute(
        'UPDATE message SET unread = 0 WHERE id = ?', (message_id,)
    )
    db.commit()


def get_received_message(user_id: int, message_id: int, db: Connection) -> Any:
    return db.execute(
        '''
        SELECT m.id, (SELECT username FROM user WHERE id = m.sender_id) AS 'from',
            created, subject, message
        FROM message m JOIN user u
        ON m.receiver_id = u.id
        WHERE m.receiver_id = ? AND m.id = ?
        ''', (user_id, message_id)
    ).fetchone()


def get_sent_message(user_id: int, message_id: int, db: Connection) -> Any:
    return db.execute(
        '''
        SELECT m.id, (SELECT username FROM user WHERE id = m.receiver_id) AS 'to',
            created, subject, message
        FROM message m JOIN user u
        ON m.sender_id = u.id
        WHERE m.sender_id = ? AND m.id = ?
        ''', (user_id, message_id)
    ).fetchone()


def delete_message(user_id: int, message_id: int, db: Connection) -> None:
    # if connected user_id is the receiver or sender of the message, delete it
    db.execute(
        '''
        DELETE FROM message 
        WHERE id = ? AND (sender_id = ? OR receiver_id = ?)
        ''', (message_id, user_id, user_id)
    )
    db.commit()