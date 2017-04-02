r"""Run this file \o/."""
from homeserver import app
import pytest
import sys

if len(sys.argv) < 1:
    raise AttributeError('Please provide an option')

if sys.argv[1] not in ['run', 'tests']:
    raise AttributeError('Option not supported')


if sys.argv[1] == 'run':
    app.run(host='0.0.0.0')

if sys.argv[1] == 'tests':
    pytest.main()
