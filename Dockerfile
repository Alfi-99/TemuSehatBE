# Gunakan Python 3.12 official image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy kode dan requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port (Railway akan override PORT env)
EXPOSE 8000

# Run FastAPI tanpa start.sh
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
