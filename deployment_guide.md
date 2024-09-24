# Deployment Guide for Inventory Management SaaS on Google Cloud VM

## Prerequisites
- Google Cloud Platform account with activated billing
- Internet access

## Setup Instructions

### 1. Create a New Project on Google Cloud Platform
- Log in to Google Cloud Platform.
- Create a new project and provide the necessary details like Project name, Project ID, and Billing account.

### 2. Activate Cloud Shell
- Click on the Activate Cloud Shell icon on the Google Cloud Platform homepage.

### 3. Clone the Repository
- Use the Cloud Shell to clone your FastAPI repository:
  ```
  git clone https://github.com/your-repo/InventoryManagementSaaS.git
  ```

### 4. Create and Activate a Virtual Environment
- Navigate to the backend directory:
  ```
  cd InventoryManagementSaaS/home/ubuntu/inventory_management
  ```
- Create a virtual environment:
  ```
  virtualenv env
  ```
- Activate the virtual environment:
  ```
  source env/bin/activate
  ```

### 5. Install Backend Requirements
- Install the necessary modules:
  ```
  pip install -r requirements.txt
  ```

### 6. Deploy FastAPI on Google App Engine
- Ensure you have an `app.yaml` file with the necessary configuration.
- Deploy the app using the command:
  ```
  gcloud app deploy app.yaml
  ```

### 7. Set Up Frontend
- Navigate to the frontend directory:
  ```
  cd ../inventory-frontend
  ```
- Install frontend dependencies:
  ```
  npm install
  ```

### 8. Deploy Frontend
- Use the `<deploy_frontend>` command to deploy the frontend.

### 9. Access the Deployed App
- Your app will be available at `your-project-id.appspot.com`.

## Additional Notes
- Ensure all environment variables are set correctly, including `DATABASE_URL` and `SECRET_KEY`.
- Configure CORS settings to allow communication between frontend and backend.
- The `app.yaml` file should include environment variables and automatic scaling settings.
