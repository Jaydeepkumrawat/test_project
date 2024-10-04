from django.test import TestCase

# Create your tests here.

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from inventory.models import InventoryItem
from accounts.models import Account
import logging

logger = logging.getLogger('inventory')

class InventoryTests(APITestCase):

    def setUp(self):
        # Create a test user and login to get the JWT token
        self.user = Account.objects.create_user(username='testuser', password='testpassword')
        
        # Obtain JWT token
        url = reverse('login')
        response = self.client.post(url, {'username':'testuser', 'password':'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data, 'resdata')

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create sample inventory item for testing
        self.item = InventoryItem.objects.create(name="Test Item", quantity=1, description="A test item", price=20)

        # URLs for the views
        self.list_create_url = reverse('item-list-create')
        self.detail_url = reverse('item-details', kwargs={'pk': self.item.id})

    def test_list_inventory_items(self):
        """
        Ensure we can list inventory items.
        """
        response = self.client.get(self.list_create_url)
        # print(response.data, 'resdata2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTrue(len(response.data['data']) > 0)
        logger.debug('List inventory items test passed.')

    def test_create_inventory_item(self):
        """
        Ensure we can create a new inventory item.
        """
        data = {'name': 'New Item', 'quantity': 1, 'description': 'A new test item', 'price': 20}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.data, {
            "status": True,
            "data": {
                "id": 2,
                "name": "New Item",
                "description": "A new test item",
                "quantity": 1,
                "price": "20.00"
            },
            "detail": "Item created successfully"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        logger.debug('Create inventory item test passed.')

    def test_retrieve_inventory_item(self):
        """
        Ensure we can retrieve an existing inventory item by ID.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Test Item')
        logger.debug('Retrieve inventory item test passed.')

    def test_update_inventory_item(self):
        """
        Ensure we can update an existing inventory item.
        """
        data = {'name': 'Updated Item', 'quantity': 15}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Item')
        self.assertEqual(response.data['data']['quantity'], 15)
        logger.debug('Update inventory item test passed.')

    def test_delete_inventory_item(self):
        """
        Ensure we can delete an existing inventory item.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        logger.debug('Delete inventory item test passed.')
