from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id' ,
                  'slug',
                  'name' ,
                  'image' ,
                  'price' ,
                  'description' ,
                  'inventory' ,
                  'featured' ,
                  ]
        extra_kwargs = {
            'url': {'view_name': 'contents-detail'}
        }

