from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    OrderCreate ,
    OrderItemCreate ,
    OrderUpdate ,
    OrderDelete
)

app_name = 'orders'

urlpatterns = [
    path('create/' , OrderCreate.as_view() , name='order-create') ,
    path('update/' , OrderUpdate.as_view() , name='order-update') ,
    path('delete/' , OrderDelete.as_view() , name='order-delete') ,
    path('create-item/' , OrderItemCreate.as_view() , name='order-create-item')
]
