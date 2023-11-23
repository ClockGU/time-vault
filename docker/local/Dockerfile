FROM python:3.10-alpine

ENV POETRY_VERSION=1.3.2 POETRY_VIRTUALENVS_CREATE=false POETRY_HOME="/opt/poetry"
ENV PATH="$PATH:$POETRY_HOME/bin"

WORKDIR /code

RUN apk add curl

RUN curl -sSL https://install.python-poetry.org  | python3 -
COPY pyproject.toml poetry.lock /
RUN poetry install
COPY ./time_vault /code/time_vault

CMD ["poetry", "run", "uvicorn", "time_vault.main:app", "--host", "0.0.0.0", "--port", "8000"]
