import pytest
from .conftest import client, clean_state


def test_is_alive(client):
    response = client.get("health")
    assert response.status_code == 200