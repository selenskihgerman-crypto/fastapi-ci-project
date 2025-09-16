import pytest
from tests.factories import ClientFactory, ParkingFactory
from app.models import Client, Parking


def test_create_client_with_factory(client, db):
    initial_count = db.session.query(Client).count()

    client_obj = ClientFactory()
    db.session.commit()

    assert db.session.query(Client).count() == initial_count + 1
    assert client_obj.id is not None
    assert client_obj.name is not None


def test_create_parking_with_factory(client, db):
    initial_count = db.session.query(Parking).count()

    parking = ParkingFactory()
    db.session.commit()

    assert db.session.query(Parking).count() == initial_count + 1
    assert parking.id is not None
    assert parking.count_places == parking.count_available_places


def test_multiple_clients_with_factory(client, db):
    clients = ClientFactory.create_batch(5)
    db.session.commit()

    assert len(clients) == 5
    assert all(client.id is not None for client in clients)


def test_parking_availability(client, db):
    parking = ParkingFactory(count_places=10)
    db.session.commit()

    assert parking.count_available_places == 10


def test_create_client_with_factory_api(client, db):
    client_data = ClientFactory.build()
    response = client.post('/clients', json={
        'name': client_data.name,
        'surname': client_data.surname,
        'credit_card': client_data.credit_card,
        'car_number': client_data.car_number
    })
    assert response.status_code == 201


def test_create_parking_with_factory_api(client, db):
    parking_data = ParkingFactory.build()
    response = client.post('/parkings', json={
        'address': parking_data.address,
        'opened': parking_data.opened,
        'count_places': parking_data.count_places
    })
    assert response.status_code == 201