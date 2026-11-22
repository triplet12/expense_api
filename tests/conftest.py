import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import expenses, categories


@pytest.fixture(autouse=True)
def clean_state():
    expenses.clear()
    categories.clear()
    yield


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def created_categories(client):
    created = []
    for name in ["Еда", "Развлечения", "Вода"]:
        r = client.post("/categories", json={"name": name})
        assert r.status_code == 201
        created.append(r.json())
    return created