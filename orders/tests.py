from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from menus.models import Menu, MenuItem, Category
from orders.models import Order, OrderItem

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='1234', role='customer')
        self.caterer = User.objects.create_user(email='caterer@test.com', password='1234', role='caterer')

        self.client.login(email='user@test.com', password='1234')

        self.category = Category.objects.create(name='Drinks')
        self.menu = Menu.objects.create(caterer=self.caterer, title='Test Menu', description='Desc')
        self.item = MenuItem.objects.create(
            menu=self.menu,
            name='Smoothie',
            description='Mango',
            price=5.0,
            category=self.category,
            stock_quantity=10
        )

    def test_create_order_success(self):
        url = reverse('orders-list')
        data = {
            "items": [
                {
                    "menu_item": self.item.id,
                    "quantity": 2
                }
            ],
            "payment_method": "cash"
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.first().quantity, 2)

    def test_create_order_insufficient_stock(self):
        url = reverse('orders-list')
        data = {
            "items": [
                {
                    "menu_item": self.item.id,
                    "quantity": 20  # more than in stock
                }
            ],
            "payment_method": "cash"
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not have enough stock", response.data[0])
