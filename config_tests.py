"""Public configuration for app."""

import os

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance/test_app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
