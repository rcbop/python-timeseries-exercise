FROM python:3.11-alpine as base
RUN adduser -D app
USER app

WORKDIR /app/

COPY --chown=app:app requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app pyproject.toml .
COPY --chown=app:app consumer/. /app/consumer/

RUN pip install --no-cache-dir -e .
ENTRYPOINT ["python", "/app/consumer/main.py"]

FROM base AS test
COPY --chown=app:app /tests/. /app/tests/
COPY --chown=app:app requirements-dev.txt /app/
RUN pip install -r requirements-dev.txt
RUN pytest -v /app/tests/
