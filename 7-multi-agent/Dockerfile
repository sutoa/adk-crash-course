FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PORT=8081
ENV PYTHONPATH=/app

# Run the application with uvicorn
CMD uvicorn app:app --host 0.0.0.0 --port $PORT 