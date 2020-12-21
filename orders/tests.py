from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Order , OrderItem
from products.models import Product


User = get_user_model()

class OrderTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='tester1' , password='tt123456' , phone_number='09121115522')
        self.user2 = User.objects.create_user(username='tester2' , password='mm321654' , phone_number='09121115523')
        self.product1 = Product.objects.create(name='product1' , price=10)
        self.product2 = Product.objects.create(name='product2' , price=20)

    @staticmethod
    def get_client():
        client = APIClient()
        # client.login(username=self.user.username , password='somepassword')   # for session authentication
        return client

    def test_order_item_create(self):
        client = self.get_client()

        # Login tester1:
        response = client.post('/api/token/' ,
                               data={
                                   'username': 'tester1' ,
                                   'password': 'tt123456'
                               })
        self.assertEqual(response.status_code , 200)
        self.assertTrue('access' in response.data)
        token = response.data['access']

        # Create Order:
        client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        order_create_response = client.post('/api/orders/create/' , data=None)
        self.assertEqual(order_create_response.status_code , 201)
        order_qs = Order.objects.all()
        self.assertEqual(order_qs.count() , 1)
        order = order_qs.first()
        self.assertEqual(order.user , self.user1)

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
        self.assertEqual(order_item_update_response.status_code , 200)
        order_item = OrderItem.objects.filter(order=order , item=1).first()
        self.assertEqual(order_item.quantity , 3)

        # Create another OrderItem:
        order_item_create_response = client.post('/api/orders/create-item/' ,
                                                 data={
                                                     "item":     "2" ,
                                                     "quantity": "5"
                                                 } ,
                                                 format='json'
                                                 )
        self.assertEqual(order_item_create_response.status_code , 201)
        order_item = OrderItem.objects.filter(order=order , item=2).first()
        self.assertEqual(order_item.item.price , 20)

        # Create another Order user1:
        order_create_duplicate_response = client.post('/api/orders/create/' , data=None)
        self.assertEqual(order_create_duplicate_response.status_code , 409)
        order_qs = Order.objects.all()
        self.assertEqual(order_qs.count() , 1)

        # Update Order user1:
        order = Order.objects.filter(user=self.user1).first()
        self.assertFalse(order.checkout)
        order_update_response = client.post('/api/orders/update/' , data=None)
        self.assertEqual(order_update_response.status_code , 200)
        order = Order.objects.filter(user=self.user1).first()
        self.assertTrue(order.checkout)

        # Login user2:
        login_user2_response = client.post('/api/token/' ,
                                           data={
                                               'username': 'tester2' ,
                                               'password': 'mm321654'
                                           })
        self.assertEqual(login_user2_response.status_code , 200)
        self.assertTrue('access' in login_user2_response.data)
        token_user2 = login_user2_response.data['access']

        # Create Order user2:
        client.credentials(HTTP_AUTHORIZATION=f'JWT {token_user2}')
        order_create_user2_response = client.post('/api/orders/create/' , data=None)
        self.assertEqual(order_create_user2_response.status_code , 201)
        order_qs = Order.objects.all()
        self.assertEqual(order_qs.count() , 2)
        order_user2 = order_qs.filter(pk=2).first()
        self.assertEqual(order_user2.user , self.user2)

        # Delete Order user2:
        order_delete_user2_response = client.post('/api/orders/delete/' , data=None)
        self.assertEqual(order_delete_user2_response.status_code , 204)
        order_qs = Order.objects.all()
        self.assertEqual(order_qs.count() , 1)

        # Delete Order user2 AGAIN:
        order_delete_user2_response = client.post('/api/orders/delete/' , data=None)
        self.assertEqual(order_delete_user2_response.status_code , 404)
