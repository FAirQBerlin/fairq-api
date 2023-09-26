# fairq-api

This API provides hourly air quality predictions for Berlin the next couple of days. There are 6 endpoints available:

- health
- stations
- streets
- grid
- lor
- simulation

Also there's a documentation page of the endpoints available if you navigate to `/docs`.

There are two versions of the API available:
- DEV Version (only internally availabe)
- PROD Version (public available): https://api.fairq.inwt-statistics.de/docs#/

## Structure

- `cache`: the currently cached files with the predictions

- `fairqapi`: API functionality
  - `cache`: scripts containing the caching logic
  - `db`: functionality to connect to the database (used by cache)
  - `internal`: helper functions
  - `logging_config`: configuration for the logs
  - `routers`: here live the files for the endpoints, one for each (they are bundled in `main.py`)
  - `schemas`: the structure of the requests to the API as well as it's response to them is structurally checked by Pydantic, these schemas are templates for the checks
  - `tests`: test files to check the performance of the endpoints as well as their output

## Local Development

Before starting the api locally, it is necessary to initialize the cache via running the script [update_cache.py](https://github.com/FAirQBerlin/fairq-api/blob/main/update-cache.py)



Start API local via

```
uvicorn fairqapi.main:app --reload
```

## Versioning

Update (calender) version with [bumpver](https://github.com/mbarkhau/bumpver):

```
bumpver update [--dry] --patch
```
`--dry` just shows how the version WOULD change. Without `--dry` the update is committed and pushed.

## Code Style & Formatting

### Style Guide

[wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide)

Usage:

```
flake8 .
```

### Formatting

#### Code Formatting

[Black](https://black.readthedocs.io/)

Usage:

```
black --line-length 120 .
```

#### Sorting Imports

[isort](https://pycqa.github.io/isort/)

Usage:
```
# check
isort --check-only .

# actually sort
isort .
```


## Cache

The API does not call the database directly but uses a cache in a Kubernetes empty-dir volume.

- With every deployment of the API there is an init job which populates the cache from the clickhouse database (`init-api-cache`)
- Another process updates the cache every hour in a sidecar container (`update-api-cache`)
- Within the api we spin up a process which watches the cache folder for modified files every minute. If a file is modified the data is loaded into memory
- Requests to the API are answered by using the in memory cache



