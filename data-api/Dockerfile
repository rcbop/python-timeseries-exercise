FROM python:3-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml .
COPY setup.py .
COPY /api/*.py /app/api/
RUN pip install -e .
ENTRYPOINT [ "python", "/app/api/main.py" ]
