import numpy as np
import pandas as pd


def transform_raw_data(df_raw: pd.DataFrame, endpoint: str, forecast_interval_in_hours: int) -> pd.DataFrame:
    """
    Formats raw api data and makes it ready for json conversion.

    :param pd.DataFrame df_raw: raw api data as queried from fairq_prod_output.api_* tables
    :param str endpoint:
    :param forecast_interval_in_hours: integer determines in which time interval the prediction is updated in hours.
    :return: pd.Dataframe: transformed api data as DataFrame, ready for json conversion
    """
    df = add_forecast_range_iso(df=df_raw, forecast_interval_in_hours=forecast_interval_in_hours)
    df = add_date_time_forecast_iso(df=df).rename(columns={"pm25": "pm2.5"})

    if endpoint == "stations":
        df = df.sort_values(["station_id"]).loc[:, ["x", "y", *get_property_cols(endpoint)]]
    elif endpoint == "grid":
        df = df.sort_values(["id"]).loc[:, ["x", "y", *get_property_cols(endpoint)]]
    elif endpoint == "streets":
        df = df.sort_values(["element_nr"]).loc[:, ["geometry", *get_property_cols(endpoint)]]
    elif endpoint == "lor":
        df = df.sort_values(["PLR_ID"]).loc[:, ["geometry", *get_property_cols(endpoint)]]
    elif endpoint == "simulation":
        df = df.rename(columns={"pm25_0": "pm2.5_0","pm25_10": "pm2.5_10", "pm25_20": "pm2.5_20",
        "pm25_30": "pm2.5_30", "pm25_40": "pm2.5_40", "pm25_50": "pm2.5_50", "pm25_60": "pm2.5_60",
        "pm25_70": "pm2.5_70", "pm25_80": "pm2.5_80", "pm25_90": "pm2.5_90", "pm25_100": "pm2.5_100"})
        df = df.sort_values(["element_nr"]).loc[:, ["geometry", *get_property_cols(endpoint)]]
    else:
        raise ValueError(
            "Incorrect endpoint '{}' was given. Possible endpoints are 'stations', 'grid', 'streets', 'lor', 'simulation'".format(endpoint)
        )

    return df


def get_iso_format() -> dict:
    """
    Returns format and name of iso8601.

    :return: dict with keys "name" and "format" of iso
    """
    return {"name": "iso8601", "format": "%Y-%m-%dT%H:%M:%S.%fZ"}


def add_forecast_range_iso(df: pd.DataFrame, forecast_interval_in_hours: int) -> pd.DataFrame:
    """
    Creates forecast range column in iso format

    :param df: pd.DataFrame must contain cols  "first_pred_date_time" and "last_pred_date_time" as type datetime64
    :param forecast_interval_in_hours: integer determines in which time interval the prediction is updated in hours.
    :return: pd.DataFrame just like input df but with one additional last column "forecast_range_isoXXXX" (object)
    """
    iso = get_iso_format()

    df["forecast_horizon_delta"] = df["last_pred_date_time"] - df["first_pred_date_time"]

    # forecast horizon in hours plus 1 to match length of list of pollutant predictions:
    df["forecast_horizon_h"] = (df["forecast_horizon_delta"] / np.timedelta64(forecast_interval_in_hours, "h")).astype("Int64") + 1
    df["forecast_horizon_h"] = df["forecast_horizon_h"].astype(str)

    df["first_pred_date_time_iso"] = df["first_pred_date_time"].dt.strftime(iso["format"]).astype(str)
    df["forecast_range_" + iso["name"]] = (
        "R" + df["forecast_horizon_h"] + "/" + df["first_pred_date_time_iso"] + "/PT" + str(forecast_interval_in_hours) + "H"
    )
    df = df.drop(
        columns=[
            "forecast_horizon_delta",
            "forecast_horizon_h",
            "first_pred_date_time_iso",
        ]
    )

    return df


def add_date_time_forecast_iso(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates forecast range column in iso format (for example iso8601 "2022-10-18T11:00:00")

    :param df: pd.DataFrame must contain col "date_time_forecast" of type datetime64
    :return: pd.DataFrame just like input df but with 'date_time_forecast' col replaced by 'forecast_range_isoXXXX' col
    of type (object).
    """
    iso = get_iso_format()

    df["date_time_forecast"] = df["date_time_forecast"].dt.strftime(iso["format"]).astype(str)
    df = df.rename(columns={"date_time_forecast": "date_time_forecast_" + iso["name"]})

    return df


def get_property_cols(endpoint: str) -> list[str]:
    """
    Returns a list of column names that shall be turned from DataFrame columns into json properties.

    :param str endpoint: Either "stations", "grid" or "streets" as str
    :return: List of column names that shall be turned into json properties
    """
    iso = get_iso_format()
    date_time_forecast_iso = "date_time_forecast_" + iso["name"]
    forecast_range_iso = "forecast_range_" + iso["name"]
    pollutants = ["no2", "pm10", "pm2.5"]
    simulation_columns = ["no2_0", "no2_10", "no2_20", "no2_30", "no2_40", "no2_50", "no2_60", "no2_70", "no2_80", "no2_90", "no2_100",
                          "pm10_0", "pm10_10", "pm10_20", "pm10_30", "pm10_40", "pm10_50", "pm10_60", "pm10_70", "pm10_80", "pm10_90", "pm10_100",
                          "pm2.5_0", "pm2.5_10", "pm2.5_20", "pm2.5_30", "pm2.5_40", "pm2.5_50", "pm2.5_60", "pm2.5_70", "pm2.5_80", "pm2.5_90", "pm2.5_100"
    ]

    standard_property_cols = [date_time_forecast_iso, forecast_range_iso, *pollutants]

    if endpoint == "stations":
        property_cols = ["station_id", *standard_property_cols]
    elif endpoint == "grid":
        property_cols = ["id", *standard_property_cols]
    elif endpoint == "streets":
        property_cols = ["element_nr", *standard_property_cols]
    elif endpoint == "lor":
        property_cols = ["PLR_ID", *standard_property_cols]
    elif endpoint == "simulation":
        property_cols = ["element_nr", date_time_forecast_iso, forecast_range_iso, *simulation_columns]
    else:
        raise ValueError("Incorrect endpoint name {} was given to pick property columns.".format(endpoint))

    return property_cols
