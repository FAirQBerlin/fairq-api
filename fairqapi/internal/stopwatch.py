"""Stopwatch context manager that logs the passed time for given label."""
import logging
from time import time


class Stopwatch(object):
    """Context wrapper class which will log the passed time and the given label."""

    def __init__(self, label: str = "<Missing Label>"):
        """Context manager needs the label to assign the elapsed_time to the right process.
        :param str label: name of the process for which to stop the time.
        """
        self.label = label

    def __enter__(self):
        """Start timer on entering the context."""
        self.elapsed_time = time()
        return self

    def __exit__(
        self,
        type,  # noqa: WPS125 (allow type name, needed for __exit__ to work)
        value,  # noqa: WPS110 (allow wrong variable name, needed for __exit__ to work)
        traceback,
    ):
        """After finishing the with... block, safe the elapsed time."""
        self.elapsed_time = round(time() - self.elapsed_time, 1)
        logging.debug({"label": self.label, "elapsed_time": self.elapsed_time})
