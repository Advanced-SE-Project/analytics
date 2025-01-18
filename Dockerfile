#------------------------------------------------------------------------------
# Dockerfile for the Analytics microservice
#------------------------------------------------------------------------------

# Use an official Python runtime as a parent image.
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements first (for caching)
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY . /app/

# Expose the port (optional for local clarity)
EXPOSE 5000

# Default command to run the application
CMD ["python", "src/app.py"]