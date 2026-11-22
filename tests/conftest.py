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