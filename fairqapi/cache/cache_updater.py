import logging
import pickle
from logging.config import dictConfig

from fairqapi.db.db_connect import db_connect
from fairqapi.internal.data_utils import get_property_cols, transform_raw_data
from fairqapi.internal.json_utils import df_to_geojson
from fairqapi.logging_config.logger_config import get_logger_config

dictConfig(get_logger_config())


class CacheUpdater():
    """
    This class updates the cache files with data from the clickhouse database
    """

    def __init__(self):
        # after how many seconds should cache invalidate?
        self.cache_invalidation_time = 3600

    def update_cache_files(self):
        """
        Update all files (stations, grid, streets) regularly. The schedule
        is defined by self.cache_invalidation_time
        """

        logging.info("Updating stations")
        self.update_stations_file()

        logging.info("Updating grid")
        self.update_grid_file()

        logging.info("Updating streets")
        self.update_streets_file()

        logging.info("Updating LOR")
        self.update_lor_file()

        logging.info("Updating simulation")
        self.update_simulation_file()

    @staticmethod
    def save_cache_file(data, filename):
        with open(f"cache/{filename}.pickle", "wb") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def update_stations_file(self):
        """get data for stations endpoint."""
        with db_connect() as db:
            stations_df_raw = db.query_dataframe("select * from api_stations final;")

        stations_df = transform_raw_data(stations_df_raw, endpoint="stations", forecast_interval_in_hours=1)

        stations_geojson = df_to_geojson(stations_df, get_property_cols("stations"))

        self.save_cache_file(stations_geojson, "stations")

    def update_grid_file(self):
        """get data for grid endpoint."""
        with db_connect() as db:
            grid_df_raw = db.query_dataframe(
                "select * from api_grid final;",
            )

        grid_df_raw.sort_values(by=["date_time_forecast", "x", "y"], inplace=True)
        grid_df = transform_raw_data(grid_df_raw, endpoint="grid", forecast_interval_in_hours=1)

        grid_geojson = df_to_geojson(grid_df, get_property_cols("grid"))

        self.save_cache_file(grid_geojson, "grid")

    def update_streets_file(self):
        """get data for streets endpoint."""
        with db_connect() as db:
            streets_df_raw = db.query_dataframe(
                "select * from api_streets final;",
            )

        streets_df_raw.sort_values(by=["date_time_forecast", "element_nr"], inplace=True)
        streets_df = transform_raw_data(streets_df_raw, endpoint="streets", forecast_interval_in_hours=1)

        streets_geojson = df_to_geojson(
            streets_df,
            get_property_cols("streets"),
            geometry_type="LineString",
        )

        self.save_cache_file(streets_geojson, "streets")

    def update_lor_file(self):
        """get data for lor endpoint."""
        with db_connect() as db:
            lor_df_raw = db.query_dataframe(
                "select * from api_lor final;",
            )

        lor_df_raw.sort_values(by=["date_time_forecast", "PLR_ID"], inplace=True)
        lor_df = transform_raw_data(lor_df_raw, endpoint="lor", forecast_interval_in_hours=24)

        lor_geojson = df_to_geojson(
            lor_df,
            get_property_cols("lor"),
            geometry_type="MultiPolygon",
        )

        self.save_cache_file(lor_geojson, "lor")

    def update_simulation_file(self):
        """get data for simulation endpoint"""
        with db_connect() as db:
            simulation_df_raw = db.query_dataframe(
                "select * from api_simulation final;"
            )
        simulation_df_raw.sort_values(by=["date_time_forecast", "element_nr"], inplace=True)
        simulation_df = transform_raw_data(simulation_df_raw, endpoint="simulation", forecast_interval_in_hours=24)

        simulation_geojson = df_to_geojson(
            simulation_df,
            get_property_cols("simulation"),
            geometry_type="LineString",
        )

        self.save_cache_file(simulation_geojson, "simulation")
