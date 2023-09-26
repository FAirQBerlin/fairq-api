# Choose base python3.10 template from dockerhub
FROM python:3.10

# install pipenv to use for package management
RUN pip3 install pipenv

# set default working directory in the container and copy all files into it
WORKDIR /usr/src/app

COPY . .

# install required packages into the pip environment of the docker container (--system)
RUN set -ex && pipenv install --deploy --system

# expose Port 8004 and start the app using gunicorn
EXPOSE 8000

CMD ["uvicorn", "fairqapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
