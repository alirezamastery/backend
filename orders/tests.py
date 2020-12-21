from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Order , OrderItem
from products.models import Product

# Create your tests here.
User = get_user_model()


class OrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester' , password='tt123456' , phone_number='09121115522')
        self.product1 = Product.objects.create(name='car' , price=10)

    @staticmethod
    def get_client():
        client = APIClient()
        # client.login(username=self.user.username , password='somepassword')   # for session authentication
        return client

    def test_order_item_create(self):
        client = self.get_client()

        # Login:
        response = client.post('/api/token/' ,
                               data={
                                   'username': 'tester' ,
                                   'password': 'tt123456'
                               })
        self.assertEqual(response.status_code , 200)
        self.assertTrue('access' in response.data)

        # Create Order:
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        order_creation_response = client.post('/api/orders/create/' , data=None)
        self.assertEqual(order_creation_response.status_code , 201)
        order = Order.objects.filter(pk=1).first()
        self.assertEqual(order.user , self.user)

        # Create OrderItem:
        order_item_create_response = client.post('/api/orders/create-item/' ,
                                                 data={
                                                     "item":     "1" ,
                                                     "quantity": "2"
                                                 } ,
                                                 format='json'
                                                 )
        self.assertEqual(order_item_create_response.status_code , 201)
        order_item = OrderItem.objects.filter(item=1).first()
        self.assertEqual(order_item.item.price , 10)

        # Update OrderItem:
        order_item_update_response = client.post('/api/orders/create-item/' ,
                                                 data={
                                                     "item":     "1" ,
                                                     "quantity": "3"
                                                 } ,
                                                 format='json'
                                                 )
        self.assertEqual(order_item_update_response.status_code , 202)
        order_item = OrderItem.objects.filter(item=1).first()
        self.assertEqual(order_item.quantity , 3)
