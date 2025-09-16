import pytest
from datetime import datetime, timedelta
from app import create_app
from app.models import db as _db, Client, Parking, ClientParking


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def test_client(db):
    client = Client(
        name='John',
        surname='Doe',
        credit_card='1234567890123456',
        car_number='A123BC'
    )
    db.session.add(client)
    db.session.commit()
    return client


@pytest.fixture
def test_parking(db):
    parking = Parking(
        address='Test Street 123',
        opened=True,
        count_places=10,
        count_available_places=10
    )
    db.session.add(parking)
    db.session.commit()
    return parking


@pytest.fixture
def test_client_parking(db, test_client, test_parking):
    client_parking = ClientParking(
        client_id=test_client.id,
        parking_id=test_parking.id,
        time_in=datetime.now() - timedelta(hours=2)
    )
    db.session.add(client_parking)
    db.session.commit()
    return client_parking