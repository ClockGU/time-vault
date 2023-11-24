FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

ENV POETRY_VERSION=1.3.2 POETRY_VIRTUALENVS_CREATE=false POETRY_HOME="/opt/poetry"
ENV PATH="$PATH:$POETRY_HOME/bin"

WORKDIR /code

RUN apt update && apt install -y curl

RUN curl -sSL https://install.python-poetry.org  | python3 -
COPY pyproject.toml poetry.lock /
RUN poetry install
COPY ./time_vault /app/app

