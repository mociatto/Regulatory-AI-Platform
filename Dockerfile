# Use an official Python runtime as a parent image
# This provides a lightweight Python 3.9 environment with minimal OS overhead
FROM python:3.9-slim

# Set the working directory in the container
# All subsequent commands will be executed from this directory
WORKDIR /app

# Copy the requirements file into the container at /app
# This is done separately from the rest of the code for Docker layer caching optimization
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir reduces the image size by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
# This includes main.py, config.py, ai_processor.py, and other project files
COPY . .

# Define the command to run the application
# This is the default command that executes when the container starts
CMD ["python", "main.py"] 