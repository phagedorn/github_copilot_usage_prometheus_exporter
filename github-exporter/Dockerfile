# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Create a user and group
# Avoid using notations like `USER 1001:1001` since it doesn't ensure the user exists
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Change the ownership of the /app directory to the appuser
RUN chown -R appuser:appuser /app

# Use pip to install any needed packages specified in requirements.txt
# As the root user, before switching to a non-root user
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-root user
USER appuser

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD [ "python", "./github-copilot-usage-prometheus-exporter.py" ]