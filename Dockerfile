# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application with gunicorn 
# Change temporary directory to /dev/shm and set minimum workers to 2 to increase performance 
# according to https://stackoverflow.com/questions/58942398/docker-running-a-flask-app-via-gunicorn-worker-timeouts-poor-performance
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "--workers", "2", "--worker-tmp-dir", "/dev/shm", "app:app"]