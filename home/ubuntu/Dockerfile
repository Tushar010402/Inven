# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    redis-server \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Kafka
RUN wget https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz \
    && tar xzf kafka_2.13-3.8.0.tgz \
    && mv kafka_2.13-3.8.0 /kafka \
    && rm kafka_2.13-3.8.0.tgz

# Copy project
COPY . /app/

# Change working directory to inventory_management
WORKDIR /app/inventory_management

# Expose ports
EXPOSE 8000 9092 6379

# Start services
CMD ["sh", "-c", "service redis-server start && /kafka/bin/zookeeper-server-start.sh /kafka/config/zookeeper.properties & /kafka/bin/kafka-server-start.sh /kafka/config/server.properties & python manage.py runserver 0.0.0.0:8000"]
