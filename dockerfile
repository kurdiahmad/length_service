# Use a smaller base image to reduce size
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy only necessary files to avoid unnecessary cache busting
COPY requirements.txt .

# Install dependencies with no cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the necessary ports
EXPOSE 8081

# Use Gunicorn for better performance
#CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8081", "length_service:app"]
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8081", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "length_service:app"]
