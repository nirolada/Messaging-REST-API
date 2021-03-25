worker: gunicorn gettingstarted.wsgi
worker: export FLASK_APP=app
worker: flask init-db
worker: gunicorn 'app:create_app()'