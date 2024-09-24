from rest_framework import serializers
from .models import Client, Store, InventoryItem

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'contact_email', 'contact_phone', 'created_at', 'updated_at']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'client', 'name', 'location', 'created_at', 'updated_at']

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'store', 'name', 'quantity', 'price', 'created_at', 'updated_at']
