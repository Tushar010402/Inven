from django.contrib import admin
from .models import Client, Store, InventoryItem

# Register your models here.
admin.site.register(Client)
admin.site.register(Store)
admin.site.register(InventoryItem)
