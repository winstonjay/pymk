import os
import tempfile

import pytest

from pymk import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    print(db_fd, db_path)
    app = create_app(SQLALCHEMY_DATABASE_URI='sqlite:///test.db')
    yield app
    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()