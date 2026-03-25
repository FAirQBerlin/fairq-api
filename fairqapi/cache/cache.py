import asyncio
import logging
import pickle
import time
import traceback
from logging.config import dictConfig
from pathlib import Path

from fairqapi.logging_config.logger_config import get_logger_config

dictConfig(get_logger_config())
logger = logging.getLogger(__name__)


class Cache:
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
        logger.info("Loading cached files into memory")

        if self.update_needed("stations"):
            logger.debug("Updating stations")
            self.stations = self.load_stations()
        else:
            logger.debug("No update needed for stations")

        if self.update_needed("grid"):
            logger.debug("Updating grid")
            self.grid = self.load_grid()
        else:
            logger.debug("No update needed for grid")

        if self.update_needed("streets"):
            logger.debug("Updating streets")
            self.streets = self.load_streets()
        else:
            logger.debug("No update needed for streets")

        if self.update_needed("lor"):
            logger.debug("Updating LOR")
            self.lor = self.load_lor()
        else:
            logger.debug("No update needed for LOR")

        if self.update_needed("simulation"):
            logger.debug("Updating simulation")
            self.simulation = self.load_simulation()
        else:
            logger.debug("No update needed for simulation")

        self.last_cache_update = time.time()

    def cache_is_loaded(self):
        return (
            self.streets is not None and self.grid is not None and self.stations is not None and self.lor is not None and self.simulation is not None
        )

    async def load_cache_files_loop(self):
        """
        reload cache files every minute if updated
        """
        while True:
            try:
                await asyncio.sleep(60)

                self.load_cache_files()
            except Exception:
                logger.exception("Something went wrong when loading cache files")
                logger.exception(traceback.format_exc())
                logger.info("Retrying ...")

    def update_needed(self, filename):
        """
        check if file was modified since last cache update
        """
        last_modification = Path(f"cache/{filename}.pickle").stat().st_mtime
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
        with Path(f"cache/{filename}.pickle").open("rb") as handle:
            return pickle.load(handle)  # noqa: S301


# initialize cache to be used everywhere
cache = Cache()
