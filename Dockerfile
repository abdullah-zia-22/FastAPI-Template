# Use the official Python image as base image
FROM python:3.11-slim

# Arguments to be passed during the build
ARG DB_HOST
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG ENVIRONMENT

# Set environment variables using build arguments
ENV DB_HOST=${DB_HOST}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}
ENV ENVIRONMENT=${ENVIRONMENT}

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local code into the container at /app
COPY . /app/

# Expose port 8000 for the FastAPI application
EXPOSE 5000

# Command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
