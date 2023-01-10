FROM python:3.11-alpine as base
WORKDIR /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml .
COPY sensor/. /app/sensor/
RUN pip install --no-cache-dir -e .
ENTRYPOINT ["python", "/app/sensor/main.py"]

FROM base AS test
COPY /tests/. /app/tests/
COPY requirements-dev.txt /app/
RUN pip install -r requirements-dev.txt
RUN pytest -v /app/tests/
