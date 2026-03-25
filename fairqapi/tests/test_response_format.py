"""Testing for some response fields.
This is not done in Pydantic because the API behaviour should not be influenced
by a failure in the schema validation for these specific fields."""

from fastapi.testclient import TestClient

from fairqapi.main import app
from fairqapi.tests.test_helper_functions import (
    validate_datetime_in_response,
    validate_forecast_range_in_response,
)

client = TestClient(app)


def test_stations_fields():
    """Test stations datetime and forecast range fields in response."""
    # act
    response = client.get("stations")
    response_json = response.json()

    # assert
    assert validate_datetime_in_response(response_json)
    assert validate_forecast_range_in_response(response_json)


def test_streets_fields():
    """Test streets datetime and forecast range fields in response."""
    # act
    response = client.get("streets")
    response_json = response.json()

    # assert
    assert validate_datetime_in_response(response_json)
    assert validate_forecast_range_in_response(response_json)


def test_simulation_fields():
    """Test simulation datetime and forecast range fields in response."""
    # act
    response = client.get("simulation")
    response_json = response.json()

    # assert
    assert validate_datetime_in_response(response_json)
    assert validate_forecast_range_in_response(response_json)


def test_lor_fields():
    """Test lor datetime and forecast range fields in response."""
    # act
    response = client.get("lor")
    response_json = response.json()

    # assert
    assert validate_datetime_in_response(response_json)
    assert validate_forecast_range_in_response(response_json)


def test_grid_fields():
    """Test grid datetime and forecast range fields in response."""
    # act
    response = client.get("grid")
    response_json = response.json()

    # assert
    assert validate_datetime_in_response(response_json)
    assert validate_forecast_range_in_response(response_json)
