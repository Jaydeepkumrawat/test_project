from django.urls import path
from .views import InventoryItemListCreateView, InventoryItemDetailView

urlpatterns = [
    path('items/', InventoryItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', InventoryItemDetailView.as_view(), name='item-details'),
]
