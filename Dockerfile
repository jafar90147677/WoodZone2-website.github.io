# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (change if needed)
EXPOSE 8080

# Run your app (replace with your actual app start command)
CMD ["python", "app.py"]
