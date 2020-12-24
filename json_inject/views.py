from django.shortcuts import render , get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .models import Category , Sample
from .serializers import CategorySerializer , SampleSerializer
from .pagination import CustomPaginationBase


class CategoryPagination(CustomPaginationBase):
    model_class = Category

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    ordering = ['id']


class SamplePagination(CustomPaginationBase):
    model_class = Sample

class SampleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sample.objects.all().order_by('id')
    serializer_class = SampleSerializer
    pagination_class = SamplePagination
    ordering = ['id']

class CpuListView(generics.ListAPIView):

    serializer_class = SampleSerializer
    # filter_backends = [
    #     SearchFilter ,
    #     DjangoFilterBackend ,
    #     OrderingFilter ,
    # ]
    # search_fields = ['name']
    # ordering_fields = ['created_date' , 'price']
    # ordering = ['-created_date']

    # pagination_class = CustomPagination

    def get_queryset(self):
        category = Category.objects.get(name='AMD')
        queryset = category.sample_set.all()
        return queryset


@api_view(['GET'])
def sample_list_view(request , *args , **kwargs):
    qs = Sample.objects.all()
    if not qs.exists():
        return Response({} , status=404)
    serializer = SampleSerializer(qs , many=True)
    return Response(serializer.data , status=200)


@api_view(['GET'])
def sample_list_view(request , *args , **kwargs):
    qs = Sample.objects.all()
    if not qs.exists():
        return Response({} , status=404)
    serializer = SampleSerializer(qs , many=True)
    return Response(serializer.data , status=200)


@api_view(['GET'])
def sample_detail_view(request , sample_id , *args , **kwargs):
    obj = get_object_or_404(Sample , pk=sample_id)
    if not obj:
        return Response({} , status=404)
    serializer = SampleSerializer(obj)
    return Response(serializer.data , status=200)
