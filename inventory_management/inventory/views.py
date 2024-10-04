import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import InventoryItemSerializer
from .models import InventoryItem

# Initialize logger
logger = logging.getLogger('inventory')

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 5)

# List and Create Inventory Items
class InventoryItemListCreateView(APIView):

    def get(self, request, *args, **kwargs):
        cache_key = 'all_inventory_items'
        cached_items = cache.get(cache_key)

        if cached_items:
            logger.info('Fetched all inventory items from cache.')
            return Response({'status': True, 'data': cached_items, 'detail': 'Items list'}, status=status.HTTP_200_OK)

        # Fetch from database if not cached
        items = InventoryItem.objects.all()
        serializer = InventoryItemSerializer(items, many=True)

        # Cache the result
        cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
        logger.info('Fetched all inventory items from database and cached the result.')

        return Response({'status': True, 'data': serializer.data, 'detail': 'Items list'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = InventoryItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Remove the cached list after a new item is created
            cache.delete('all_inventory_items')
            logger.info('Created new inventory item and invalidated cached list.')

            return Response({'status': True, 'data': serializer.data, 'detail': 'Item created successfully'}, status=status.HTTP_201_CREATED)

        logger.error(f'Error creating inventory item: {serializer.errors}')
        return Response({'status': False, 'error': serializer.errors, 'detail': 'Error creating item'}, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, Update, and Delete Inventory Items
class InventoryItemDetailView(APIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    lookup_field = 'id'

    def get_object(self, pk):
        try:
            return InventoryItem.objects.get(pk=pk)
        except InventoryItem.DoesNotExist:
            logger.warning(f'Item with id {pk} not found.')
            raise NotFound({
                'status': False, 
                'data': [], 
                'detail': f'No item found with id {pk}', 
                'status': status.HTTP_404_NOT_FOUND
            })

    def get(self, request, pk, *args, **kwargs):
        cache_key = f'inventory_item_{pk}'
        # print(cache_key,'cache_key ')
        cached_item = cache.get(cache_key)

        if cached_item:
            logger.info(f'Fetched item {pk} from cache.')
            return Response({'status': True, 'data': cached_item, 'detail': 'Item details'}, status=status.HTTP_200_OK)

        # Retrieve from DB and cache it
        obj = self.get_object(pk=pk)
        serializer = InventoryItemSerializer(obj)
        cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
        logger.info(f'Fetched item {pk} from database and cached it.')
        return Response({'status': True, 'data': serializer.data, 'detail': 'Item details'}, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        serializer = InventoryItemSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            cache.delete(f'inventory_item_{pk}')  # Remove cache and updated item
            logger.info(f'Updated item {pk} and remove cache.')
            return Response({'status': True, 'data': serializer.data, 'detail': 'Item updated successfully'}, status=status.HTTP_200_OK)

        logger.error(f'Error updating item {pk}: {serializer.errors}')
        return Response({
            'status': False, 
            'error': serializer.errors, 
            'detail': 'Something went wrong'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        obj.delete()
        cache.delete(f'inventory_item_{pk}')  
        logger.info(f'Item {pk} deleted')
        return Response({'status': True, 'data': [], 'detail': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    