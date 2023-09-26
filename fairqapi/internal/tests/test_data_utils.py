"""
test file for data_utils.py.
"""

import pandas as pd
from pandas.testing import assert_frame_equal

from fairqapi.internal.data_utils import (
    add_date_time_forecast_iso,
    add_forecast_range_iso,
    transform_raw_data,
)


def test_add_date_time_forecast_iso() -> None:
    """This test asserts correct creation of time_forecast column in iso format."""
    # 1. arrange
    df = pd.DataFrame(
        {
            "date_time_forecast": [
                pd.Timestamp("2022-10-24 13:00:00"),
                pd.Timestamp("2022-10-25 16:00:00"),
            ],
        },
    )

    expected_df = pd.DataFrame(
        {
            "date_time_forecast_iso8601": [
                "2022-10-24T13:00:00.000000Z",
                "2022-10-25T16:00:00.000000Z",
            ],
        }
    )

    # 2. act
    res = add_date_time_forecast_iso(df)

    # 3. assert
    assert_frame_equal(res, expected_df)


def test_add_forecast_range_iso() -> None:
    """This test asserts correct creation of forecast range column in iso format."""
    # 1. arrange
    df = pd.DataFrame(
        {
            "first_pred_date_time": [
                pd.Timestamp("2022-10-24 14:00:00"),
                pd.Timestamp("2022-10-24 12:00:00"),
            ],
            "last_pred_date_time": [
                pd.Timestamp("2022-10-24 16:00:00"),
                pd.Timestamp("2022-10-25 22:00:00"),
            ],
        },
    )

    expected_df = pd.DataFrame(
        {
            "first_pred_date_time": [
                pd.Timestamp("2022-10-24 14:00:00"),
                pd.Timestamp("2022-10-24 12:00:00"),
            ],
            "last_pred_date_time": [
                pd.Timestamp("2022-10-24 16:00:00"),
                pd.Timestamp("2022-10-25 22:00:00"),
            ],
            "forecast_range_iso8601": [
                "R3/2022-10-24T14:00:00.000000Z/PT1H",
                "R35/2022-10-24T12:00:00.000000Z/PT1H",
            ],
        }
    )

    # 2. act
    res = add_forecast_range_iso(df, forecast_interval_in_hours=1)

    # 3. assert
    assert_frame_equal(res, expected_df)


def test_transform_raw_data_stations() -> None:
    """This test asserts correct output format for /stations endpoint."""

    # 1. arrange
    df = pd.DataFrame(
        {
            "station_id": ["174"],
            "x": [396182],
            "y": [5819313],
            "date_time_forecast": [pd.Timestamp("2022-10-24 13:00:00")],
            "first_pred_date_time": [pd.Timestamp("2022-10-24 14:00:00")],
            "last_pred_date_time": [pd.Timestamp("2022-10-24 15:00:00")],
            "no2": [[32.6, 30.4]],
            "pm10": [[21.7, 21.2]],
            "pm2.5": [[21.7, 21.2]],
        },
    )

    expected_df = pd.DataFrame(
        {
            "x": [396182],
            "y": [5819313],
            "station_id": ["174"],
            "date_time_forecast_iso8601": ["2022-10-24T13:00:00.000000Z"],
            "forecast_range_iso8601": ["R2/2022-10-24T14:00:00.000000Z/PT1H"],
            "no2": [[32.6, 30.4]],
            "pm10": [[21.7, 21.2]],
            "pm2.5": [[21.7, 21.2]],
        }
    )

    # 2. act
    res = transform_raw_data(df, endpoint="stations", forecast_interval_in_hours=1)

    # 3. assert
    assert_frame_equal(res, expected_df)


def test_transform_raw_data_grid() -> None:  # noqa: WPS210 WPS218
    """This test asserts correct output format for /grid endpoint."""

    # 1. arrange
    df = pd.DataFrame(
        {
            "id": [1],
            "x": [396182],
            "y": [5819313],
            "date_time_forecast": [pd.Timestamp("2022-10-24 13:00:00")],
            "first_pred_date_time": [pd.Timestamp("2022-10-24 14:00:00")],
            "last_pred_date_time": [pd.Timestamp("2022-10-24 15:00:00")],
            "no2": [[32.6, 30.4]],
            "pm10": [[21.7, 21.2]],
            "pm2.5": [[21.7, 21.2]],
        },
    )

    expected_df = pd.DataFrame(
        {
            "x": [396182],
            "y": [5819313],
            "id": [1],
            "date_time_forecast_iso8601": ["2022-10-24T13:00:00.000000Z"],
            "forecast_range_iso8601": ["R2/2022-10-24T14:00:00.000000Z/PT1H"],
            "no2": [[32.6, 30.4]],
            "pm10": [[21.7, 21.2]],
            "pm2.5": [[21.7, 21.2]],
        }
    )

    # 2. act
    res = transform_raw_data(df, endpoint="grid", forecast_interval_in_hours=1)

    # 3. assert
    assert_frame_equal(res, expected_df)


def test_transform_raw_data_streets() -> None:  # noqa: WPS210 WPS218
    """This test asserts correct output format for /streets endpoint."""

    # 1. arrange
    df = pd.DataFrame(
        {
            "element_nr": ["47420012_47420011.02"],
            "date_time_forecast": [pd.Timestamp("2022-10-30 22:18:00")],
            "first_pred_date_time": [pd.Timestamp("2022-10-30 14:00:00")],
            "last_pred_date_time": [pd.Timestamp("2022-11-02 21:00:00")],
            "no2": [[44.6, 45.2, 46.1]],
            "pm10": [[57.5, 61.4, 81.1]],
            "pm25": [[31.8, 31.1, 29.1]],
            "geometry": [
                '{"type":"LineString",'
                '"coordinates":'
                "[[392123.4,5807250.7],"
                "[392143.3,5807248.6],"
                "[392163.2,5807248.3],"
                "[392214.4,5807253.1]]}"
            ],
        }
    )

    expected_df = pd.DataFrame(
        {
            "geometry": [
                '{"type":"LineString",'
                '"coordinates":[[392123.4,5807250.7],[392143.3,5807248.6],[392163.2,5807248.3],[392214.4,5807253.1]]}'
            ],
            "element_nr": ["47420012_47420011.02"],
            "date_time_forecast_iso8601": ["2022-10-30T22:18:00.000000Z"],
            "forecast_range_iso8601": ["R80/2022-10-30T14:00:00.000000Z/PT1H"],
            "no2": [[44.6, 45.2, 46.1]],
            "pm10": [[57.5, 61.4, 81.1]],
            "pm2.5": [[31.8, 31.1, 29.1]],
        }
    )

    # 2. act
    res = transform_raw_data(df, endpoint="streets", forecast_interval_in_hours=1)

    # 3. assert
    assert_frame_equal(res, expected_df)
