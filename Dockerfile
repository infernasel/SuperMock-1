FROM python:3.10-slim

LABEL maintainer="SuperMock Team"
LABEL description="SuperMock - Local Telegram Bot API Mock Server"

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Install the application
RUN pip install -e .

# Expose default port
EXPOSE 8081

# Set environment variables
ENV SUPERMOCK_HOST=0.0.0.0
ENV SUPERMOCK_PORT=8081

# Run the server
CMD ["supermock", "server", "--host", "0.0.0.0", "--port", "8081"]
