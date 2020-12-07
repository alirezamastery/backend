from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view , authentication_classes , permission_classes

from .models import Product
from .serializers import ProductSerializer


# class ProductViewSet(ModelViewSet):



def product_list_view(request):
    qs = Product.objects.all()
    if not qs.exists():
        return Response({} , status=404)
    serializer = ProductSerializer(qs , many=True)
    return Response(serializer , status=200)
