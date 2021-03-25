import os
from flask import Flask

from . import db, auth, messages


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    flask_env = os.getenv('FLASK_ENV', 'development').lower()
    app.config.from_mapping(
        SECRET_KEY=os.urandom(16) if flask_env == 'production' else flask_env,
        DATABASE=os.path.join(app.instance_path, 'app.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/isalive')
    def isalive():
        return 'Messaging REST API is up!'

    db.init_app(app)  # register db with the application
    app.register_blueprint(auth.bp)
    app.register_blueprint(messages.bp)

    return app
