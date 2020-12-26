from django.shortcuts import render , get_object_or_404
from rest_framework import viewsets , generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Category , Sample , Genre , Band
from .serializers import CategorySerializer , SampleSerializer , GenreSerializer , BandSerializer
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

    def get_queryset(self):
        category = Category.objects.get(name='CPU')
        total = list()
        if category.get_children():
            for cat in category.get_children():
                qs = Category.objects.get(name=cat)
                total.append(qs.objects.all())

        print(total)
        return total


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.filter(level=0).order_by('id')


class BandView(generics.RetrieveAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer

    def get_object(self):
        print('in get_object')
        rs = self.kwargs
        for k in rs:
            print(f'{k:<20} | {self.kwargs.get(k)}')
        parent1 = Genre.objects.get(name=self.kwargs.get('slug1'))
        print(parent1.level)
        parent2 = Genre.objects.get(name=self.kwargs.get('slug2'))
        print(parent2)
        return Band.objects.get(pk=self.kwargs.get('pk'))


# @api_view(['GET'])
# def band_list_view(request , slug,id)


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
