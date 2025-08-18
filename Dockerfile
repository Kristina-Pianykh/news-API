FROM python:3.13.7 as build
WORKDIR /build

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.13.7-slim
ENV APP_HOST ${APP_HOST:-"0.0.0.0"}
ENV APP_PORT ${APP_PORT:-8000}
WORKDIR /api
COPY --from=build /build/requirements.txt ./
# install Cython below 3.0 and pin PyYaml to 6.0 (current version in poetry.lock)
# subject to change once https://github.com/yaml/pyyaml/issues/601 is resolved
RUN pip install "Cython<3.0" "pyyaml==6.0" --no-build-isolation
RUN pip install -r requirements.txt
COPY news_api .

# expose port
# EXPOSE 8000

ENTRYPOINT uvicorn --host $APP_HOST api:app
