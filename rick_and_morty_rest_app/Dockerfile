FROM python:3

MAINTAINER Matan Moshe

WORKDIR /app

# Copy everything from the current directory (app folder) to the WORKDIR
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN echo ${BUILD_NUMBER} && pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5050

# Set build arguments and environment variables
ARG BUILD_NUMBER
ENV ENVIRONMENT=DEV

# Run the application
ENTRYPOINT ["python", "app.py"]
