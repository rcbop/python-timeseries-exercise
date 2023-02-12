FROM python:3-alpine AS api
RUN pip install --upgrade pip

RUN adduser -D app
USER app

WORKDIR /app

COPY --chown=app:app requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app pyproject.toml .
COPY --chown=app:app /api/. /app/api/

RUN pip install --no-cache-dir -e .
ENTRYPOINT [ "python", "/app/api/main.py" ]

FROM api AS test
COPY --chown=app:app /tests/. /app/tests/
COPY --chown=app:app requirements-dev.txt /app/
RUN pip install -r requirements-dev.txt
RUN pytest -v /app/tests/
