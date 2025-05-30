FROM python:3.12-slim AS base

ENV POETRY_VERSION=2.1.1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_HOME="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"
ENV PATH="/root/.local/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache \
    pip install pipx && pipx ensurepath

FROM base AS builder

RUN --mount=type=cache,target=/root/.cache \
    pipx install "poetry==$POETRY_VERSION"

WORKDIR "$PYSETUP_HOME"
COPY ./pyproject.toml ./poetry.lock ./
COPY ./pgload ./pgload

RUN --mount=type=cache,target=$POETRY_HOME/pypoetry/.cache \
    touch README.md && poetry build --format wheel --no-interaction --no-ansi

FROM base AS runtime

COPY --from=builder $PYSETUP_HOME/dist/pgload-*.whl /tmp/
COPY run.sh /
RUN --mount=type=cache,target=/root/.cache \
    pipx install /tmp/pgload-*.whl && rm -rf /tmp/pgload-*.whl && chmod +x /run.sh

# Expose metrics port
EXPOSE 8080

CMD ["/bin/bash", "/run.sh"]
