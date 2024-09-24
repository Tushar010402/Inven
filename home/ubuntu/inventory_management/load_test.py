from locust import HttpUser, task, between
from random import randint

class InventoryUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Authenticate user
        response = self.client.post("/api/token/", json={
            "username": "testuser",
            "password": "testpassword"
        })
        self.token = response.json()["access"]
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def view_clients(self):
        self.client.get("/api/clients/")

    @task(2)
    def view_stores(self):
        self.client.get("/api/stores/")

    @task(4)
    def view_inventory_items(self):
        self.client.get("/api/inventory-items/")

    @task(1)
    def create_inventory_item(self):
        self.client.post("/api/inventory-items/", json={
            "store": randint(1, 10),  # Assuming stores with IDs 1-10 exist
            "name": f"Test Item {randint(1, 1000)}",
            "quantity": randint(1, 100),
            "price": round(randint(100, 10000) / 100, 2)
        })

    @task(2)
    def update_inventory_item(self):
        item_id = randint(1, 100)  # Assuming inventory items with IDs 1-100 exist
        self.client.put(f"/api/inventory-items/{item_id}/", json={
            "quantity": randint(1, 100),
            "price": round(randint(100, 10000) / 100, 2)
        })

    @task(1)
    def delete_inventory_item(self):
        item_id = randint(1, 100)  # Assuming inventory items with IDs 1-100 exist
        self.client.delete(f"/api/inventory-items/{item_id}/")

if __name__ == "__main__":
    import os
    os.system("locust -f load_test.py")
