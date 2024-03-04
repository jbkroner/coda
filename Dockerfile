# Use an official Python 3.11 runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install .

EXPOSE 8000

# Run coda.py when the container launches
CMD ["python", "./src/coda/coda.py"]
