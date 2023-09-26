import asyncio
import logging
import os
import pickle
import time
import traceback
from logging.config import dictConfig

from fairqapi.logging_config.logger_config import get_logger_config

dictConfig(get_logger_config())

class Cache():
    """
    This class contains the cached values for all endpoints. It also
    contains functionality to update the cached values if the files in the storage
    are updated
    """

    def __init__(self):
        self.last_cache_update = 0
        self.stations = None
        self.streets = None
        self.grid = None
        self.lor = None
        self.simulation = None
        self.load_cache_files()


    def load_cache_files(self):
        logging.info("Loading cached files into memory")

        if self.update_needed("stations"):
            logging.debug("Updating stations")
            self.stations = self.load_stations()
        else:
            logging.debug("No update needed for stations")

        if self.update_needed("grid"):
            logging.debug("Updating grid")
            self.grid = self.load_grid()
        else:
            logging.debug("No update needed for grid")

        if self.update_needed("streets"):
            logging.debug("Updating streets")
            self.streets = self.load_streets()
        else:
            logging.debug("No update needed for streets")

        if self.update_needed("lor"):
            logging.debug("Updating LOR")
            self.lor = self.load_lor()
        else:
            logging.debug("No update needed for LOR")

        if self.update_needed("simulation"):
            logging.debug("Updating simulation")
            self.simulation = self.load_simulation()
        else:
            logging.debug("No update needed for simulation")

        self.last_cache_update = time.time()

    def cache_is_loaded(self):
        return (
            self.streets is not None and
            self.grid is not None and
            self.stations is not None and
            self.lor is not None and
            self.simulation is not None
        )

    async def load_cache_files_loop(self):
        """
        reload cache files every minute if updated
        """
        while True:
            try:
                await asyncio.sleep(60)

                self.load_cache_files()
            except Exception as e:
                logging.error("Something went wrong when loading cache files")
                logging.error(traceback.format_exc())
                logging.info("Retrying ...")

    def update_needed(self, filename):
        """
        check if file was modified since last cache update
        """
        last_modification = os.path.getmtime(f"cache/{filename}.pickle")

        return last_modification > self.last_cache_update

    def load_stations(self):
        return self.load_cache_file("stations")

    def load_grid(self):
        return self.load_cache_file("grid")

    def load_streets(self):
        return self.load_cache_file("streets")

    def load_lor(self):
        return self.load_cache_file("lor")

    def load_simulation(self):
        return self.load_cache_file("simulation")

    @staticmethod
    def load_cache_file(filename):
        with open(f"cache/{filename}.pickle", "rb") as handle:
           return pickle.load(handle)


# initialize cache to be used everywhere
cache = Cache()
