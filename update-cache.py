import datetime
import sys
import time


from fairqapi.cache.cache_updater import CacheUpdater


def main(loop=False):
    """
    This function updates pickle files with data from clickhouse db.
    The API uses the data from pickle files to prevent too many requests
    to the database.
    """

    cache_updater = CacheUpdater()
    
    if loop:
        while True:
            now = datetime.datetime.now()

            # update every 45th minute of every hour
            if now.minute == 45:
                cache_updater.update_cache_files()
            
            now = datetime.datetime.now()

            # sleep until next minute. Add 10 secs to be sure to be in next minute
            time.sleep(60 - now.second + 10)

    else:
        cache_updater.update_cache_files()


if __name__ == "__main__":
    # This is executed when run from the command line
    loop = len(sys.argv) > 1 and sys.argv[1] == "loop"

    main(loop=loop)