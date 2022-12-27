FROM python:3-alpine
WORKDIR /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml .
COPY setup.py .
COPY generator/*.py /app/generator/
RUN pip install -e .
ENTRYPOINT ["python", "/app/generator/main.py"]
