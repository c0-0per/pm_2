# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
# Add the parent directory to PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app/backend:/app/frontend"

# Run app.py when the container launches
CMD ["python", "backend/App.py"]
