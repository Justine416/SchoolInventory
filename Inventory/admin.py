from django.contrib import admin
from .models import Item, Transaction

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'count')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'user_name', 'action', 'quantity', 'date')
    list_filter = ('action', 'date')
    search_fields = ('user_name', 'item__name')
