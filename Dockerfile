FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y git curl ffmpeg wget bash && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run bot
CMD ["python3", "-m", "devgagan"]
