import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture(scope="function")
def client():
    # Создаем таблицы для тестов
    Base.metadata.create_all(bind=engine)
    
    client = TestClient(app)
    yield client
    
    # Очищаем после тестов
    Base.metadata.drop_all(bind=engine)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item(client):
    item_data = {"name": "Test Item", "description": "Test Description"}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
