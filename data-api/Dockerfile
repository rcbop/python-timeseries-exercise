FROM python:3-alpine AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml .
COPY /api/. /app/api/
RUN pip install -e .
ENTRYPOINT [ "python", "/app/api/main.py" ]

FROM base AS test
COPY /tests/. /app/tests/
COPY requirements-dev.txt /app/
RUN pip install -r requirements-dev.txt
RUN pytest -v /app/tests/
