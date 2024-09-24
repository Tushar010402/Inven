# Docker Run Instructions for Inventory Management SaaS

## Backend
To run the backend Docker container, use the following command:
```bash
docker run -p 5000:5000 inventory-backend
```

## Frontend
To run the frontend Docker container, use the following command:
```bash
docker run -p 3000:3000 inventory-frontend
```

Ensure both containers are running simultaneously to allow the frontend to communicate with the backend.
