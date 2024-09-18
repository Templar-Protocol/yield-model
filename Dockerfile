# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
# Cloud Run will automatically set the PORT environment variable
EXPOSE 8080

# Command to run the application
# Use the PORT environment variable provided by Cloud Run
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
