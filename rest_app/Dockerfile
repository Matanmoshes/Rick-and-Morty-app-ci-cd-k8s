# Start from a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose the port Flask will run on
EXPOSE 5010

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5010"]
