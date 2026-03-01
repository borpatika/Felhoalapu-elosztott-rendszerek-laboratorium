# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

# Expose port
EXPOSE 8080

# Run the server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080"]