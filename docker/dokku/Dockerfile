FROM python:3.10-slim

ENV POETRY_VERSION=1.3.2 POETRY_VIRTUALENVS_CREATE=false POETRY_HOME="/opt/poetry"
ENV PATH="$PATH:$POETRY_HOME/bin"

RUN groupadd app --gid 32767
RUN adduser --ingroup app --home /app --uid 32767 --disabled-password --gecos "" app

RUN apt update && apt install -y curl

RUN curl -sSL https://install.python-poetry.org  | python3 -
COPY pyproject.toml poetry.lock /
RUN poetry install

USER app
COPY --chown=app:app . /app
WORKDIR /app

CMD ["fastapi", "run", "time_vault/main.py","--host", "0.0.0.0", "--port", "5000"]

