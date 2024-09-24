from django.test import TestCase
from inventory.models import Client, Store, InventoryItem

class TestClientModel(TestCase):
    def test_client_creation(self):
        client = Client.objects.create(
            name="Test Client",
            contact_email="test@example.com",
            contact_phone="1234567890"
        )
        self.assertEqual(client.name, "Test Client")
        self.assertEqual(client.contact_email, "test@example.com")
        self.assertEqual(client.contact_phone, "1234567890")

class TestStoreModel(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            name="Test Client",
            contact_email="test@example.com",
            contact_phone="1234567890"
        )

    def test_store_creation(self):
        store = Store.objects.create(
            client=self.client,
            name="Test Store",
            location="Test Location"
        )
        self.assertEqual(store.client, self.client)
        self.assertEqual(store.name, "Test Store")
        self.assertEqual(store.location, "Test Location")

class TestInventoryItemModel(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            name="Test Client",
            contact_email="test@example.com",
            contact_phone="1234567890"
        )
        self.store = Store.objects.create(
            client=self.client,
            name="Test Store",
            location="Test Location"
        )

    def test_inventory_item_creation(self):
        item = InventoryItem.objects.create(
            store=self.store,
            name="Test Item",
            quantity=10,
            price=9.99
        )
        self.assertEqual(item.store, self.store)
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.price, 9.99)
