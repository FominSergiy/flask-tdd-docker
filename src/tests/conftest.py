import pytest

from src import create_app, db

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        yield app # the tess happen here

@pytest.fixture(scope='module')
def test_database():
    db.create_all()
    yield db

    db.session.remove()
    db.drop_all()
