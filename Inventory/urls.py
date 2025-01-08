from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import get_inventory, inventory, add_item, manage_transaction, transaction_list, take_item, return_item, manage_inventory, home

urlpatterns = [
    path('', views.home,name='home'),
    path('inventory/', inventory, name='inventory'),
    path('add-item/', add_item, name='add_item'),
    path('manage-transaction/', manage_transaction, name='manage_transaction'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('take-item/', take_item, name='take_item'),
    path('return-item/', return_item, name='return_item'),
    path('manage-inventory/', manage_inventory, name='manage_inventory'),
    path('api/inventory/', get_inventory, name='get_inventory'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),



]
