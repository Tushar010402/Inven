import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from inventory.models import Client, Store, InventoryItem
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestInventoryIntegration:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpass')

    @pytest.fixture
    def client_data(self):
        return {
            'name': 'Test Client',
            'contact_email': 'test@example.com',
            'contact_phone': '1234567890'
        }

    @pytest.fixture
    def store_data(self, client):
        return {
            'client': client.id,
            'name': 'Test Store',
            'location': 'Test Location'
        }

    @pytest.fixture
    def inventory_item_data(self, store):
        return {
            'store': store.id,
            'name': 'Test Item',
            'quantity': 10,
            'price': 9.99
        }

    def test_create_client(self, api_client, user, client_data):
        api_client.force_authenticate(user=user)
        response = api_client.post(reverse('client-list'), client_data)
        assert response.status_code == 201
        assert Client.objects.count() == 1
        assert Client.objects.get().name == 'Test Client'

    def test_create_store(self, api_client, user, client_data, store_data):
        api_client.force_authenticate(user=user)
        client_response = api_client.post(reverse('client-list'), client_data)
        store_data['client'] = client_response.data['id']
        response = api_client.post(reverse('store-list'), store_data)
        assert response.status_code == 201
        assert Store.objects.count() == 1
        assert Store.objects.get().name == 'Test Store'

    def test_create_inventory_item(self, api_client, user, client_data, store_data, inventory_item_data):
        api_client.force_authenticate(user=user)
        client_response = api_client.post(reverse('client-list'), client_data)
        store_data['client'] = client_response.data['id']
        store_response = api_client.post(reverse('store-list'), store_data)
        inventory_item_data['store'] = store_response.data['id']
        response = api_client.post(reverse('inventoryitem-list'), inventory_item_data)
        assert response.status_code == 201
        assert InventoryItem.objects.count() == 1
        assert InventoryItem.objects.get().name == 'Test Item'

    def test_get_client_stores(self, api_client, user, client_data, store_data):
        api_client.force_authenticate(user=user)
        client_response = api_client.post(reverse('client-list'), client_data)
        store_data['client'] = client_response.data['id']
        api_client.post(reverse('store-list'), store_data)
        response = api_client.get(reverse('client-stores', args=[client_response.data['id']]))
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Test Store'

    def test_get_store_inventory(self, api_client, user, client_data, store_data, inventory_item_data):
        api_client.force_authenticate(user=user)
        client_response = api_client.post(reverse('client-list'), client_data)
        store_data['client'] = client_response.data['id']
        store_response = api_client.post(reverse('store-list'), store_data)
        inventory_item_data['store'] = store_response.data['id']
        api_client.post(reverse('inventoryitem-list'), inventory_item_data)
        response = api_client.get(reverse('store-inventory', args=[store_response.data['id']]))
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Test Item'
