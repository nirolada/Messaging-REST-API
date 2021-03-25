web: gunicorn gettingstarted.wsgi
web: export FLASK_APP=app
web: flask init-db
web: gunicorn 'app:create_app()'