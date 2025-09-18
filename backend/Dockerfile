# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (change if your app uses a different port)
EXPOSE 8000

# Command to run the backend (adjust as needed)
CMD ["python", "src/main.py"]