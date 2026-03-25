from re import match

INVALID_FORMAT = "Invalid datetime format. It should be 'YYYY-MM-DDThh:mm:ssZ'."
INVALID_FORECAST_RANGE = (
    "Invalid forecast range format. It should be 'R<forecast_horizon_h>/<first_pred_date_time_iso>/PT<forecast_interval_in_hours>H'."
)


def validate_datetime_format(value: str) -> str:
    """
    Validates the datetime format of the date_time_forecast_iso8601 fields in the response.

    :param datetime value: datetime object
    :return: datetime
    """
    pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    if not match(pattern, value):
        raise ValueError(INVALID_FORMAT)
    return value


def validate_forecast_range_format(value: str) -> str:
    """
    Validates the forecast_range_iso8601 fields in the response.

    :param str value: forecast_range_iso8601 string
    :return: str
    """
    pattern = r"^R(\d+)/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z/PT(1|24)H$"
    if not match(pattern, value):
        raise ValueError(INVALID_FORECAST_RANGE)
    return value


def validate_datetime_in_response(response_json):
    """Validate datetime format in response."""
    for feature in response_json["features"]:
        properties = feature["properties"]
        date_time = properties["date_time_forecast_iso8601"]
        try:
            validate_datetime_format(date_time)
        except ValueError:
            return False
    return True


def validate_forecast_range_in_response(response_json):
    """Validate forecast range format in response."""
    for feature in response_json["features"]:
        properties = feature["properties"]
        forecast_range = properties["forecast_range_iso8601"]
        try:
            validate_forecast_range_format(forecast_range)
        except ValueError:
            return False
    return True
