FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything from the socket folder to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn[standard] aio_pika

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
