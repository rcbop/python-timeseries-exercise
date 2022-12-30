FROM python:3-buster
WORKDIR /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dashboard/. /app/dashboard/
ENTRYPOINT ["python", "/app/dashboard/main.py"]
