r"""Run this file \o/."""
from homeserver import app
import pytest
import sys

if len(sys.argv) < 1:
    raise AttributeError('Please provide an option')

if sys.argv[1] not in ['runserver', 'tests']:
    raise AttributeError('Option not supported')


if sys.argv[1] == 'runserver':
    app.run(host='0.0.0.0')

if sys.argv[1] == 'tests':
    pytest.main()
