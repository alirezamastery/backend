from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view , authentication_classes , permission_classes
from rest_framework import generics
from rest_framework.filters import OrderingFilter , SearchFilter
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Product
from ..serializers import ProductSerializer
from .pagination import ListViewPagination , CustomPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):  # this class handles both list view and detail view!
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [
        SearchFilter ,
        DjangoFilterBackend ,
        OrderingFilter ,
    ]
    search_fields = ['name']
    ordering_fields = ['created_date' , 'price']
    ordering = ['-created_date']

    def get_object(self , queryset=None , **kwargs):
        item = self.kwargs.get('pk')  # the router in urls.py automatically names the variable "pk": /{pk}
        return get_object_or_404(Product , slug=item)


@api_view(['GET'])
def product_detail_view(request , slug , *args , **kwargs):
    qs = Product.objects.filter(slug=slug)
    if not qs.exists():
        return Response({} , status=404)
    obj = qs.first()
    serializer = ProductSerializer(obj)
    return Response(serializer.data , status=200)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter ,
        DjangoFilterBackend ,
        OrderingFilter ,
    ]
    search_fields = ['name']
    ordering_fields = ['created_date' , 'price']
    ordering = ['-created_date']

    pagination_class = CustomPagination


# ++++++++++++++++++++++++++ No longer used ++++++++++++++++++++++++++
@api_view(['GET'])
def product_list_view(request , *args , **kwargs):
    qs = Product.objects.all()
    if not qs.exists():
        return Response({} , status=404)
    serializer = ProductSerializer(qs , many=True)
    return Response(serializer.data , status=200)
