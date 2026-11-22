import pytest
from .conftest import client, clean_state, created_categories


def test_is_alive(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_patch_categories_id(client):
    client.post("/categories", json={"name": 'Развлечения'})
    r = client.patch("/categories/1", json = {"name": 'Вода'})
    assert r.json()["name"] == 'Вода'


def test_incorrect_patch_categories_id(client):
    client.post("/categories", json={"name": 'Развлечения'})
    r = client.patch("/categories/1", json = {})
    assert r.status_code == 422


def test_get_categories(client, created_categories):
    response = client.get("/categories")
    assert response.status_code == 200
    names = {c["name"] for c in response.json()}
    assert names == {"Еда", "Развлечения", "Вода"}


def test_incorrect_post_categories(client):
    response = client.post("/categories", json={'incorrect': 'incorrect'})
    assert response.status_code == 422


def test_incorrect_categories_id(client, created_categories):
    response = client.get("/categories/100")
    assert response.status_code == 404

