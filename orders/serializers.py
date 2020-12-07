from rest_framework import serializers

from .models import Order , OrderItem
from products.models import Product
from products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['checkout']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item' , 'quantity']

    # def to_representation(self , instance):
    #     self.fields['item'] = ProductSerializer(read_only=True)
    #     return super().to_representation(instance)

    # def create(self, validated_data):
    #     item = validated_data.pop('item')
    #     print('item:' , item)
    #     item_instance = Product.objects.filter(pk=item)
    #     order_item = OrderItem.objects.create(**validated_data , item=item_instance[0])
    #     return order_item
