# # Use the official lightweight Python image
# FROM python:3.13-slim-bullseye

# # Set work directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy app files
# COPY . .

# # Run the API
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# Use a more stable Python version
FROM python:3.13-slim-bullseye

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Run the API with the PORT environment variable
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8080}"]