from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import (
    product_list_view ,
    ProductListView ,
    product_detail_view ,
    ProductViewSet
)

router = DefaultRouter()
router.register('' , ProductViewSet , basename='product')
urlpatterns = router.urls
# how in is done in the Docs:
# urlpatterns = [
#     path('', include(router.urls)),
# ]


# urlpatterns = [
#     path('' , ProductListView.as_view() , name='product-list') ,
#     # path('' , product_list_view) ,
#     path('<str:slug>/' , product_detail_view , name='product-detail') ,
# ]
