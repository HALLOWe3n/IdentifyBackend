# pull official base image
FROM python:3.9-slim

# set work directory
WORKDIR /usr/src/

# set environments variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src/

# copy requirements file
COPY requirements.txt .

# install dependencies
RUN set -eux \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . .
