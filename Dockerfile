# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to leverage Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose port (Render will auto-assign)
EXPOSE 8000

# Start your app (FastAPI example with uvicorn)
# If Flask: change to "flask run --host=0.0.0.0 --port=8000"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
