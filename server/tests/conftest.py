import pytest
from app import create_app
from app.extensions import db as _db
from app.config import TestConfig

@pytest.fixture()
def app():
    app = create_app(TestConfig)
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()