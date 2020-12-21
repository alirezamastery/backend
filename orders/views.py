from django.http import Http404

from rest_framework import status , viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .serializers import OrderSerializer , OrderItemSerializer
from .models import Order , OrderItem
from products.models import Product


class OrderCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , format='json'):
        serializer = OrderSerializer(data=request.data)
        order_query = Order.objects.filter(user=request.user , checkout=False)
        if len(order_query) > 0:
            return Response('there is still another open order' , status=status.HTTP_409_CONFLICT)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            if order:
                json = serializer.data
                return Response(json , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class OrderUpdate(APIView):
    permission_classes = [IsAuthenticated]

    # TODO what approach is better?: 1-add checkout=True in here and just send POST from frontend
    # TODO 2-send POST from frontend with checkout=True payload
    def post(self , request , format='json'):
        # order_id = request.data['order']  # just in case we need this data
        order_query = Order.objects.filter(user=request.user , checkout=False)
        if len(order_query) != 1:
            if order_query.count() < 1:
                return Response('no open order to update' , status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('there are more than one open orders. dont know which on to close' ,
                                status=status.HTTP_409_CONFLICT)
        order = order_query.first()
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order.checkout = True
            order.save()
            if order.checkout:
                return Response(f'updated order of {request.user} to checkout={order.checkout}' ,
                                status=status.HTTP_200_OK)

        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class OrderDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , format='json'):
        # order_id = request.data['order']  # just in case we need this data
        order_query = Order.objects.filter(user=request.user , checkout=False)
        if len(order_query) != 1:
            if len(order_query) < 1:
                return Response('no open order to delete' , status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('there are more than one open orders. dont know which on to close' ,
                                status=status.HTTP_409_CONFLICT)
        order = order_query.first()
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order_deleted = order.delete()
            if order_deleted:
                json = serializer.data
                return Response(json , status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class OrderItemCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , format='json'):
        order_query = Order.objects.filter(user=request.user , checkout=False)
        if len(order_query) > 1:
            return Response('there is still another open order' , status=status.HTTP_409_CONFLICT)

        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            order = order_query.first()
            product_id = request.data['item']
            product = Product.objects.filter(pk=product_id).first()
            quantity = request.data['quantity']
            order_item , created = OrderItem.objects.update_or_create(order=order ,
                                                                      item=product ,
                                                                      defaults={"quantity": quantity})
            if created:
                json = serializer.data
                return Response(json , status=status.HTTP_201_CREATED)
            else:
                return Response(f'updated order item quantity to: {quantity}' , status=status.HTTP_200_OK)

        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


# ==================== later project ====================
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        order_query = Order.objects.filter(user=self.request.user , checkout=False)
        if len(order_query) > 0:
            return Response('there is still another open order' , status=status.HTTP_400_BAD_REQUEST)
        return order_query
