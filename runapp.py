import os

from paste.deploy import loadapp
from waitress import serve
from raven import Client
from raven.middleware import Sentry

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    sentry_url = os.environ.get('SENTRY_URL')
    app = loadapp('config:production.ini', relative_to='.')
    if sentry_url:
        app = Sentry(
        app,
        Client(sentry_url)
        )
    serve(app, host='0.0.0.0', port=port)
