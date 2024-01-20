# Use an official Python runtime as a parent image
FROM python:3.10

# Install system dependencies
RUN apt-get update
RUN apt-get install -y python3-dev

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=events_test.settings

# Run daphne when the container launches
CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "events_test.asgi:application"]