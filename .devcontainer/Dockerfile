FROM python:3.12-bullseye

# Install Docker
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Create docker group and add user to it
RUN groupadd docker || true && usermod -aG docker root

# Set up working directory
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Verify docker installation
RUN docker --version
