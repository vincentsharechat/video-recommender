FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 6006

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:6006", "--workers", "2", "--timeout", "120", "app:app"]
