"""test file for json_utils.py."""
import pandas as pd

from fairqapi.internal.json_utils import df_to_geojson


def test_df_to_geojson_point() -> None:
    """This test asserts correct output format for df_to_geojson of geometry type 'Point'."""
    # arrange
    property_cols = [
        "id",
        "date_time_forecast_iso8601",
        "forecast_range_iso8601",
        "no2",
        "pm10",
        "pm2.5",
    ]
    df = pd.DataFrame(
        {
            "x": [415725, 415725],
            "y": [5810275, 5810325],
            "id": [1, 2],
            "date_time_forecast_iso8601": [
                "2022-10-27T09:14:45.000000Z",
                "2022-10-27T09:14:45.000000Z",
            ],
            "forecast_range_iso8601": [
                "R2/2022-10-27T10:00:00.000000Z/PT1H",
                "R2/2022-10-27T10:00:00.000000Z/PT1H",
            ],
            "no2": [[22.4, 22.2], [1.4, 4.2]],
            "pm10": [[23.5, 21.8], [53.5, 2.8]],
            "pm2.5": [[42.4, 9.2], [62.4, 3.2]],
        }
    )

    expected_dict = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [415725, 5810275],
                    "crs": "EPSG:25833",
                },
                "properties": {
                    "id": 1,
                    "date_time_forecast_iso8601": "2022-10-27T09:14:45.000000Z",
                    "forecast_range_iso8601": "R2/2022-10-27T10:00:00.000000Z/PT1H",
                    "no2": [22.4, 22.2],
                    "pm10": [23.5, 21.8],
                    "pm2.5": [42.4, 9.2],
                },
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [415725, 5810325],
                    "crs": "EPSG:25833",
                },
                "properties": {
                    "id": 2,
                    "date_time_forecast_iso8601": "2022-10-27T09:14:45.000000Z",
                    "forecast_range_iso8601": "R2/2022-10-27T10:00:00.000000Z/PT1H",
                    "no2": [1.4, 4.2],
                    "pm10": [53.5, 2.8],
                    "pm2.5": [62.4, 3.2],
                },
            },
        ],
    }

    # act
    res = df_to_geojson(df, property_cols)

    # assert
    assert res == expected_dict


def test_df_to_geojson_linestring() -> None:
    """This test asserts correct output format for df_to_geojson of geometry type 'Linestring'."""
    # arrange
    property_cols = [
        "element_nr",
        "date_time_forecast_iso8601",
        "forecast_range_iso8601",
        "no2",
        "pm10",
        "pm2.5",
    ]
    df = pd.DataFrame(
        {
            "geometry": [
                '{"type":"LineString","coordinates":[[378710.2,5823451.6],[378745.3,5823439.2]]}',
                '{"type":"LineString","coordinates":[[383970.2,5834194.4],[383965.5,5834108.6]]}',
            ],
            "element_nr": ["33580039_33580041.02", "38690008_38690007.02"],
            "date_time_forecast_iso8601": [
                "2022-10-30T21:54:47.000000Z",
                "2022-10-30T19:53:25.000000Z",
            ],
            "forecast_range_iso8601": [
                "R2/2022-10-30T14:00:00.000000Z/PT1H",
                "R2/2022-10-30T14:00:00.000000Z/PT1H",
            ],
            "no2": [[51.4, 50.7], [30.9, 27.4]],
            "pm10": [[27.1, 24.1], [57.7, 53.9]],
            "pm2.5": [[33.2, 30.8], [35.6, 33.7]],
        }
    )

    expected_dict = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[378710.2, 5823451.6], [378745.3, 5823439.2]],
                    "crs": "EPSG:25833",
                },
                "properties": {
                    "element_nr": "33580039_33580041.02",
                    "date_time_forecast_iso8601": "2022-10-30T21:54:47.000000Z",
                    "forecast_range_iso8601": "R2/2022-10-30T14:00:00.000000Z/PT1H",
                    "no2": [51.4, 50.7],
                    "pm10": [27.1, 24.1],
                    "pm2.5": [33.2, 30.8],
                },
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[383970.2, 5834194.4], [383965.5, 5834108.6]],
                    "crs": "EPSG:25833",
                },
                "properties": {
                    "element_nr": "38690008_38690007.02",
                    "date_time_forecast_iso8601": "2022-10-30T19:53:25.000000Z",
                    "forecast_range_iso8601": "R2/2022-10-30T14:00:00.000000Z/PT1H",
                    "no2": [30.9, 27.4],
                    "pm10": [57.7, 53.9],
                    "pm2.5": [35.6, 33.7],
                },
            },
        ],
    }

    # act
    res = df_to_geojson(df, property_cols, geometry_type="LineString")

    # assert
    assert res == expected_dict
