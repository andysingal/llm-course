#NEED THOROUGH TESTING
# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /

# Copy the requirements file into the container at /app
COPY ./requirements.txt /requirements.txt

# Install the required packages
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Copy the current directory contents into the container at /app
COPY . /

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Start Gunicorn
CMD ["gunicorn", "main:app", "-w", "1", "-b", "0.0.0.0:8080", "--timeout", "300","--error-logfile", "error.log","--access-logfile" ,"access.log"]

