"""Initialise flask app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys


def create_app(config_name=''):
    """App Factory."""
    app = Flask(__name__, instance_relative_config=True)

    if config_name == '' or config_name == 'run':
        app.config.from_object('config_run')
        app.config.from_pyfile('config.py', silent=False)
    elif config_name == 'tests':
        app.config.from_object('config_tests')
        app.config.from_pyfile('config.py', silent=False)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


db = SQLAlchemy()

if 'tests' in sys.argv:
    config = sys.argv[1]
else:
    config = ''

app = create_app(config)

import homeserver.models
import homeserver.views
