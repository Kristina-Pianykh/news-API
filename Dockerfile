# FROM ubuntu:22.04
FROM python:3.10-slim as python-base


# make poetry install to this location
ENV POETRY_HOME="/opt/poetry" \
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    # deps for building python deps
    build-essential

# install poetry - respects $POETRY_HOME
# RUN curl -sSL https://install.python-poetry.org | python -
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python

# copy project requirement files here to ensure they will be cached.
# WORKDIR $PYSETUP_PATH
# COPY poetry.lock pyproject.toml ./


RUN mkdir app
WORKDIR /app

COPY . .

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# expose port
EXPOSE 80

WORKDIR /app/news_api

# # start app
CMD poetry run uvicorn api:app --reload