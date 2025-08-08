FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml uv.lock* ./

# Install uv for fast Python package management
RUN pip install uv

# Install Python dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/brain_memory_store /app/logs

# Set environment variables
ENV PYTHONPATH=/app/src:/app
ENV PYTHONUNBUFFERED=1

# Expose port for health checks and potential HTTP interface
EXPOSE 8000

# Health check endpoint
COPY healthcheck.py .

# Default command (can be overridden)
CMD ["uv", "run", "python", "main.py"]