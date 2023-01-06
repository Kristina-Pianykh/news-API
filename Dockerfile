FROM python:3.10-slim as python-base

# make poetry install to this location
ENV POETRY_HOME="/opt/poetry" \
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# `builder-base` stage is used to build deps + create our virtual environment
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    # deps for building python deps
    build-essential

RUN curl -sSL https://install.python-poetry.org | python -

RUN mkdir app
WORKDIR /app

COPY . .

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# expose port
EXPOSE 8000

WORKDIR /app/news_api

# # start app
CMD poetry run uvicorn api:app --reload