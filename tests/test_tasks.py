import pytest
from .conftest import client, clean_state, created_categories


def test_is_alive(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_get_categories(client, created_categories):
    response = client.get("/categories")
    assert response.status_code == 200
    names = {c["name"] for c in response.json()}
    assert names == {"Еда", "Развлечения", "Вода"}


def test_incorrect_post_categories(client):
    response = client.post("/categories", json={'incorrect': 'incorrect'})
    assert response.status_code == 422





