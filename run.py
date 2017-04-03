r"""Run this file \o/."""
from homeserver import app
import sys
import pytest

if len(sys.argv) >= 2 and sys.argv[1] == 'tests':
    pytest.main()
else:
    app.run(host='0.0.0.0')
