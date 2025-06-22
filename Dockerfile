# Use the official Python 3.10 slim image as the base image
FROM python:3.10-slim-buster

# Set the working directory inside the container to /app
WORKDIR /app

# Copy all files from the current directory to the container's /app directory
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 for the application
EXPOSE 5000

# Set the default command to run the application
CMD ["python3","app.py"]