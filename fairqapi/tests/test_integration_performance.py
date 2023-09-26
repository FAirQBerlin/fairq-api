"""Integration testing for fairqapi: performance."""

import logging

from fastapi.testclient import TestClient
from numpy import average

from fairqapi.internal.stopwatch import Stopwatch
from fairqapi.main import app

client = TestClient(app)


def test_health_performance() -> None:
    """Test health endpoint performance."""
    # arrange
    target_time = 0.5
    endpoint = "health"

    # act
    logged_time = ping_endpoint(endpoint, 3)

    # assert
    assert_timings(endpoint, logged_time, target_time)


def test_stations_performance() -> None:
    """Test stations endpoint performance."""
    # arrange
    target_time = 1
    endpoint = "stations"

    # act
    logged_time = ping_endpoint(endpoint, 3)

    # assert
    assert_timings(endpoint, logged_time, target_time)


def test_streets_performance() -> None:
    """Test streets endpoint performance."""
    # arrange
    target_time = 6
    endpoint = "streets"

    # act
    logged_time = ping_endpoint(endpoint, 3)

    # assert
    assert_timings(endpoint, logged_time, target_time)


def test_grid_performance() -> None:
    """Test grid endpoint performance."""
    # arrange
    target_time = 6
    endpoint = "grid"

    # act
    logged_time = ping_endpoint(endpoint, 3)

    # assert
    assert_timings(endpoint, logged_time, target_time)


def test_lor_performance() -> None:
    """Test lor endpoint performance."""
    # arrange
    target_time = 15
    endpoint = "lor"

    # act
    logged_time = ping_endpoint(endpoint, 3)

    # assert
    assert_timings(endpoint, logged_time, target_time)


def test_simulation_performance() -> None:
    """Test simulation endpoint performance."""
    # arrange
    target_time = 5
    endpoint = "simulation"

    # act
    logged_time = ping_endpoint(endpoint, 3)

    # assert
    assert_timings(endpoint, logged_time, target_time)


def ping_endpoint(endpoint: str, times: int):
    """Ping endpoint repeatedly (n = times) and measure how long it takes (logged_time) to respond."""
    logged_time = []
    for _ in range(times):
        with Stopwatch(label=endpoint) as timer:
            client.get(endpoint)
        logged_time.append(timer.elapsed_time)
    return logged_time


def assert_timings(endpoint: str, logged_time: list, target_time: float):
    """Assert that the logged times are on average <= the target_time."""
    average_logged_time = round(average(logged_time), 1)
    log_msg = (
        "Accessing the {endpoint} endpoint took on average {avg_time} seconds.".format(
            endpoint=endpoint,
            avg_time=average_logged_time,
        ),
    )
    if average_logged_time > target_time:
        error_msg = "{log_msg} Target time is {target_time}s. Logged times: {all_times}".format(
            log_msg=log_msg,
            target_time=target_time,
            all_times=logged_time,
        )
        raise TimeoutError(error_msg)
    logging.info(log_msg)
