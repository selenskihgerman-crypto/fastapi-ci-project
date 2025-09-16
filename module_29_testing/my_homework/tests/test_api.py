import pytest
from datetime import datetime, timedelta
from app.models import Client, Parking, ClientParking


@pytest.mark.parametrize('endpoint', [
    '/clients',
    '/clients/1'
])
def test_get_methods(client, test_client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200


def test_create_client(client, db):
    data = {
        'name': 'Alice',
        'surname': 'Smith',
        'credit_card': '9876543210987654',
        'car_number': 'B456CD'
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    assert 'id' in response.get_json()

    client_obj = db.session.get(Client, response.get_json()['id'])
    assert client_obj is not None
    assert client_obj.name == 'Alice'


def test_create_parking(client, db):
    data = {
        'address': 'New Parking 456',
        'opened': True,
        'count_places': 20
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    assert 'id' in response.get_json()

    parking = db.session.get(Parking, response.get_json()['id'])
    assert parking is not None
    assert parking.address == 'New Parking 456'
    assert parking.count_available_places == 20


@pytest.mark.parking
def test_enter_parking(client, test_client, test_parking, db):
    data = {
        'client_id': test_client.id,
        'parking_id': test_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 201

    parking = db.session.get(Parking, test_parking.id)
    assert parking.count_available_places == 9

    client_parking = ClientParking.query.filter_by(
        client_id=test_client.id,
        parking_id=test_parking.id
    ).first()
    assert client_parking is not None
    assert client_parking.time_out is None


@pytest.mark.parking
def test_exit_parking(client, test_client, test_parking, test_client_parking, db):
    data = {
        'client_id': test_client.id,
        'parking_id': test_parking.id
    }
    response = client.delete('/client_parkings', json=data)
    assert response.status_code == 200

    parking = db.session.get(Parking, test_parking.id)
    assert parking.count_available_places == 10

    client_parking = db.session.get(ClientParking, test_client_parking.id)
    assert client_parking.time_out is not None

    response_data = response.get_json()
    assert 'parking_time_hours' in response_data
    assert 'cost' in response_data


def test_enter_closed_parking(client, test_client, db):
    closed_parking = Parking(
        address='Closed Parking',
        opened=False,
        count_places=5,
        count_available_places=5
    )
    db.session.add(closed_parking)
    db.session.commit()

    data = {
        'client_id': test_client.id,
        'parking_id': closed_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400


def test_exit_without_credit_card(client, db):
    client_no_card = Client(
        name='No',
        surname='Card',
        credit_card=None,
        car_number='C789DE'
    )
    db.session.add(client_no_card)

    parking = Parking(
        address='Test Parking',
        opened=True,
        count_places=10,
        count_available_places=10
    )
    db.session.add(parking)
    db.session.commit()

    client_parking = ClientParking(
        client_id=client_no_card.id,
        parking_id=parking.id,
        time_in=datetime.now(),
        time_out=None
    )
    db.session.add(client_parking)
    db.session.commit()

    data = {
        'client_id': client_no_card.id,
        'parking_id': parking.id
    }
    response = client.delete('/client_parkings', json=data)

    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_enter_parking_no_places(client, test_client, db):
    full_parking = Parking(
        address='Full Parking',
        opened=True,
        count_places=1,
        count_available_places=0
    )
    db.session.add(full_parking)
    db.session.commit()

    data = {
        'client_id': test_client.id,
        'parking_id': full_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400


def test_enter_parking_already_parked(client, test_client, test_parking, db):
    data = {
        'client_id': test_client.id,
        'parking_id': test_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 201

    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400


def test_exit_not_parked(client, test_client, test_parking, db):
    data = {
        'client_id': test_client.id,
        'parking_id': test_parking.id
    }
    response = client.delete('/client_parkings', json=data)
    assert response.status_code == 404


def test_create_client_without_optional_fields(client, db):
    data = {
        'name': 'Minimal',
        'surname': 'Client'
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201

    client_obj = db.session.get(Client, response.get_json()['id'])
    assert client_obj.credit_card is None
    assert client_obj.car_number is None


def test_get_nonexistent_client(client):
    response = client.get('/clients/9999')
    assert response.status_code == 404