import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base


@pytest_asyncio.fixture(scope="function")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(test_db):
    with TestClient(app) as client:
        yield client


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Добро пожаловать в кулинарную книгу API"


def test_create_recipe(client):
    recipe_data = {
        "name": "Тестовый рецепт",
        "cooking_time": 30,
        "ingredients": "Тест1, Тест2",
        "description": "Тестовое описание"
    }
    response = client.post("/recipes/", json=recipe_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Тестовый рецепт"
    assert data["views"] == 0


def test_get_recipes(client):
    recipe_data = {
        "name": "Тестовый рецепт",
        "cooking_time": 30,
        "ingredients": "Тест1, Тест2",
        "description": "Тестовое описание"
    }
    client.post("/recipes/", json=recipe_data)

    response = client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Тестовый рецепт"


def test_get_recipe(client):
    recipe_data = {
        "name": "Тестовый рецепт",
        "cooking_time": 30,
        "ingredients": "Тест1, Тест2",
        "description": "Тестовое описание"
    }
    create_response = client.post("/recipes/", json=recipe_data)
    recipe_id = create_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Тестовый рецепт"
    assert data["views"] == 1