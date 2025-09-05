# Gunakan Python resmi
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements dan source
COPY requirements.txt .
COPY . .

# Install dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Set environment variable untuk Railway port
ENV PORT=8000

# Jalankan ADK api_server
CMD ["python", "-m", "google.adk.api_server", "--port", "8000"]
