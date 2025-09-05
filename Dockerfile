FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Jalankan ADK api_server
CMD ["python", "-m", "google.adk.api_server"]
