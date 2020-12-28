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


class BandFilter(FilterSet):
    in_stock = djangofilters_filters.BooleanFilter(field_name="inventory", method='is_in_stock')

    class Meta:
        model = Band
        fields = ['genre', 'color', 'brand']

    def is_in_stock(self, queryset, name, value):  # boolean True is 1 so it filters "inventory >= 1" , kind of a hack!!
        return queryset.filter(inventory__gte=value)


class BandListView(generics.ListAPIView):
    # queryset = Band.objects.all()
    serializer_class = BandSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,  # TODO only order based on certain fields
                       filters.SearchFilter]
    # filterset_fields = ['genre', 'color', 'brand']
    filterset_class = BandFilter
    search_fields = ['name']

    def get_queryset(self):
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
        # if there is search, handle it
        # if search:
        #     return qs.filter(name__contains=search)
        # else:
        #     return qs


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
