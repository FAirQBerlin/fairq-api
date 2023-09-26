"""This module contains utility functions needed for connecting to the clickhouse database."""
import logging
import os

from clickhouse_driver import Client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def db_connect() -> Client:
    """
    Return Client object for db connection to clickhouse.

    :return: Client object for db connection to clickhouse
    """
    return Client(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        secure=True,
        settings={"use_numpy": True},
    )
