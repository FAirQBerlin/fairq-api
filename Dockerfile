# Choose base python3.14 template from dockerhub
FROM python:3.14-slim

ARG DEV_DEPS=false

# no venv from poetry
ENV TZ=Europe/Berlin \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# install poetry for package and env management
RUN pip3 install poetry

# set default working directory in the container and copy all files into it
WORKDIR /usr/src/app


# Install dependencies
# dependencies only, for layer caching
COPY pyproject.toml poetry.lock* README.md ./
RUN echo "DEV_DEPS value is: ${DEV_DEPS}" && \
    # Install dependencies based on DEV_DEPS argument
    if [ "${DEV_DEPS}" = "true" ]; then \
      poetry install --with dev --no-root --no-interaction --no-ansi; \
    else \
      poetry install --without dev --no-root --no-interaction --no-ansi; \
    fi

# copy the app and build only our code
COPY . .
RUN set -ex && poetry install --only-root

# expose Port 8000 and start the app using uvicorn
EXPOSE 8000
CMD ["uvicorn", "fairqapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
