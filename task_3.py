import pytest

@pytest.fixture
def client():
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_valid_registration(client):
    response = client.post('/registration', data={
        'email': 'test@example.com',
        'phone': '1234567890',
        'name': 'Иван',
        'address': 'Москва',
        'index': '123456',
        'comment': 'Всё ок'
    })
    assert response.status_code == 200

def test_invalid_email(client):
    response = client.post('/registration', data={
        'email': 'not-email',
        'phone': '1234567890',
        'name': 'Иван',
        'address': 'Москва',
        'index': '123456',
        'comment': ''
    })
    assert response.status_code == 400
    assert 'email' in response.json

def test_invalid_phone(client):
    response = client.post('/registration', data={
        'email': 'test@example.com',
        'phone': '12345',
        'name': 'Иван',
        'address': 'Москва',
        'index': '123456',
        'comment': ''
    })
    assert response.status_code == 400
    assert 'phone' in response.json

def test_invalid_index(client):
    response = client.post('/registration', data={
        'email': 'test@example.com',
        'phone': '1234567890',
        'name': 'Иван',
        'address': 'Москва',
        'index': 'abcde',
        'comment': ''
    })
    assert response.status_code == 400
    assert 'index' in response.json

# И так далее для остальных полей
