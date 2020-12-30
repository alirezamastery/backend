from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters
from django_filters import rest_framework as django_filters_for_rest
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters.rest_framework import filters as djangofilters_filters

from .models import Category, Sample, Genre, Band
from .serializers import CategorySerializer, SampleSerializer, GenreSerializer, BandSerializer, \
    GenreSerializerRecursive
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
    # queryset = Band.objects.all()
    serializer_class = BandSerializer

    def get_object(self):
        print('in get_object')
        rs = self.kwargs
        for k in rs:
            print(f'{k:<10} | {self.kwargs.get(k)}')

        return Band.objects.get(pk=self.kwargs.get('pk'))


class GenreRoot(generics.ListAPIView):
    queryset = Genre.objects.filter(level=0)
    serializer_class = GenreSerializerRecursive


class MyBackend(DjangoFilterBackend):

    def get_schema_operation_parameters(self, view):
        parameters = super().get_schema_operation_parameters(view)

        for parameter in parameters:  # or you can directly use parameter['in'] == 'query' in the frontend!
            if parameter['in'] == 'query':
                parameter['filterable'] = True
            else:
                parameter['filterable'] = False

        return parameters


class BandFilter(FilterSet):
    in_stock = djangofilters_filters.BooleanFilter(field_name='inventory', method='is_in_stock', label='filter')
    brand = djangofilters_filters.BooleanFilter(field_name='brand', label='filter')

    class Meta:
        model = Band
        fields = ['genre', 'color']

    def __new__(cls, *args, **kwargs):  # messing with filters creation
        new_class = super().__new__(cls)
        # filters = new_class.base_filters
        # print(filters['genre'].label)
        # filters['genre'].label = 'oooooooooooooo' # if you request api and then request schema it works otherwise no
        return new_class

    def __init__(self, *args, **kwargs):  # messing with filters creation some more
        super().__init__(*args, **kwargs)
        # self.filters['genre'].label = 'sdsssssssssssssssssss'
        print(self.filters['genre'].label)

    def is_in_stock(self, queryset, name, value):  # boolean True is 1 so it filters "inventory >= 1" , kind of a hack!!
        return queryset.filter(inventory__gte=value)


class BandListView(generics.ListAPIView):
    # queryset = Band.objects.all()
    serializer_class = BandSerializer
    filter_backends = [MyBackend,
                       filters.OrderingFilter,  # TODO only order based on certain fields
                       filters.SearchFilter]
    # filterset_fields = ['genre', 'color', 'brand']
    filterset_class = BandFilter
    search_fields = ['name']

    def get_queryset(self):
        if self.kwargs.get('slug') is None:  # for schema compatibility
            return Band.objects.none()

        parent0 = Genre.objects.get(name=self.kwargs.get('slug'))
        descendants = parent0.get_descendant_count()
        search = self.request.query_params.get('search', None)
        # get leaf nodes
        if descendants:
            parent0_children = parent0.get_children().filter(children__isnull=True)
            IDs = []
            for child in parent0_children:
                IDs.append(child.id)
            qs = Band.objects.filter(genre_id__in=IDs)
        else:
            qs = parent0.leaves.all()

        return qs


@api_view(['GET'])
def sample_list_view(request, *args, **kwargs):
    qs = Sample.objects.all()
    if not qs.exists():
        return Response({}, status=404)
    serializer = SampleSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def sample_detail_view(request, sample_id, *args, **kwargs):
    obj = get_object_or_404(Sample, pk=sample_id)
    if not obj:
        return Response({}, status=404)
    serializer = SampleSerializer(obj)
    return Response(serializer.data, status=200)
