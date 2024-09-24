# Local Setup Instructions for Inventory Management SaaS

## Prerequisites
- Ensure Docker and Docker Compose are installed on your machine.

## Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd /home/ubuntu/InventoryManagementSaaS/home/ubuntu/inventory_management
   ```
2. Build the backend Docker image:
   ```bash
   docker build -t inventory-backend .
   ```
3. Run the backend Docker container:
   ```bash
   docker run -p 5000:5000 inventory-backend
   ```

## Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd /home/ubuntu/InventoryManagementSaaS/home/ubuntu/inventory-frontend
   ```
2. Build the frontend Docker image:
   ```bash
   docker build -t inventory-frontend .
   ```
3. Run the frontend Docker container:
   ```bash
   docker run -p 3000:3000 inventory-frontend
   ```

## Running the Project
- Ensure both backend and frontend containers are running simultaneously to allow communication between services.
- Access the frontend at `http://localhost:3000` and use the login credentials to test the application.

## Additional Notes
- Redis and Kafka are integrated and will run as part of the Docker Compose setup.
- Ensure all services are up and running before testing the application.
