FROM python:3-buster as base
WORKDIR /app/
COPY requirements.txt .
COPY pyproject.toml .
RUN pip install --no-cache-dir -r requirements.txt
COPY dashboard/. /app/dashboard/
ENTRYPOINT ["python", "/app/dashboard/main.py"]

FROM base AS test
COPY /tests/. /app/tests/
COPY requirements-dev.txt /app/
RUN pip install -r requirements-dev.txt
RUN pytest -v /app/tests/
