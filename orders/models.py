import datetime
from django.conf import settings
from django.db import models

from products.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

    def get_user_phone_number(self):
        return self.user.phone_number

    get_user_phone_number.short_description = 'Phone Number'

    def get_items_number(self):
        items_query = self.orderitem_set.all()
        return len(items_query)

    get_items_number.short_description = 'Number of Items'


class OrderItem(models.Model):
    order = models.ForeignKey('Order' , on_delete=models.CASCADE)
    item = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.item} | order from "{self.order}"'

# {
# "item":1,
# "quantity":7
# }
