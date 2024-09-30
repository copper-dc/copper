# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot code into the container
COPY . .

# Run the bot when the container launches
CMD [ "python", "./copper.py" ]
