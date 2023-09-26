"""Integration testing for fairqapi: responses."""

from fastapi.testclient import TestClient

from fairqapi.main import app

client = TestClient(app)


def test_health_check_response():
    """Test health endpoint response."""
    # act
    response = client.get("health")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"


def test_stations_response():
    """Test stations endpoint response."""
    # act
    response = client.get("stations")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"


def test_streets_response():
    """Test streets endpoint response."""
    # act
    response = client.get("streets")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"


def test_lor_response():
    """Test lor endpoint response."""
    # act
    response = client.get("lor")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"


def test_grid_response():
    """Test grid endpoint response."""
    # act
    response = client.get("grid")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"


def test_streets_response_limit():
    """Test streets endpoint response with limit."""
    # act
    response = client.get("streets?limit=10")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"
    assert len(response.json()["features"]) == 10


def test_grid_response_limit():
    """Test grid endpoint response with limit."""
    # act
    response = client.get("grid?limit=10")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"
    assert len(response.json()["features"]) == 10

def test_lor_response_limit():
    """Test lor endpoint response with limit."""
    # act
    response = client.get("lor?limit=10")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"
    assert len(response.json()["features"]) == 10

def test_simulation_response_limit():
    """Test simulation endpoint response with limit."""
    # act
    response = client.get("lor?limit=10")

    # assert
    assert response.status_code == 200
    assert response.encoding == "utf-8"
    assert len(response.json()["features"]) == 10
