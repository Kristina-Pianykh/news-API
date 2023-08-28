FROM python:3.11.5 as build
WORKDIR /build

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.5-slim
ENV APP_HOST ${APP_HOST:-"0.0.0.0"}
ENV APP_PORT ${APP_PORT:-8000}
WORKDIR /api
COPY --from=build /build/requirements.txt ./
RUN pip install -r requirements.txt
COPY news_api .

# expose port
# EXPOSE 8000

ENTRYPOINT uvicorn --host $APP_HOST api:app
