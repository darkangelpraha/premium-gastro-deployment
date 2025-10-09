# Premium Gastro Psychological System - Web Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs

# Set environment variables
ENV FLASK_APP=mr_plate_api_server.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose ports
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/mr-plate/health || exit 1

# Run the application
CMD ["python", "mr_plate_api_server.py"]