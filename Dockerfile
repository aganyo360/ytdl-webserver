FROM python:3.11-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Install yt-dlp
RUN pip install --no-cache-dir yt-dlp fastapi uvicorn

# Copy app
WORKDIR /app
COPY . /app

# Expose port
EXPOSE 3000


# Run the webserver
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

