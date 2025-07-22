FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy all files to /app
COPY . /app

# Install dependencies (including awscli)
RUN apt-get update && \
    apt-get install -y awscli && \
    pip install --no-cache-dir -r requirements.txt

# Default command to run your app
CMD ["python3", "app.py"]
