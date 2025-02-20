# Use a temporary image to install dependencies
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Use a clean runtime image
FROM python:3.9-slim
WORKDIR /app

# Create a non-root user and switch to it
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Copy dependencies and source code from the builder image
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Expose the necessary ports
EXPOSE 8081

# Use Gunicorn for better performance
#CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8081", "length_service:app"]
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8081", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "length_service:app"]
