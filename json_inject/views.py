from django.shortcuts import render , get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .models import Sample
from .serializers import SampleSerializer
from .pagination import CustomPagination


class SampleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    pagination_class = CustomPagination


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
