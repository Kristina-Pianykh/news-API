FROM python:3.10.9 as build
WORKDIR /build

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.9-slim
WORKDIR /api
COPY --from=build /build/requirements.txt ./
RUN pip install -r requirements.txt
COPY news_api .

# expose port
# EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "api:app"]
