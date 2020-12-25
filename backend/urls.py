from django.conf import settings
from django.contrib import admin
from django.urls import path , include
from rest_framework.schemas import get_schema_view

from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

from .serializers import MyTokenObtainPairView

urlpatterns = [
    path('admin/' , admin.site.urls) ,
    path('api/products/' , include('products.urls')) ,
    # path('' , include('users.urls')) ,
    path('api/snippets/' , include('snippets.urls')) ,
    path('api/user/' , include('users.urls')) ,
    path('api-auth/' , include('rest_framework.urls' , namespace='rest_framework')) ,
    path('api/token/' , TokenObtainPairView.as_view() , name='token_obtain_pair') ,
    path('api/token/refresh/' , TokenRefreshView.as_view() , name='token_refresh') ,
    path('api/orders/' , include('orders.urls')) ,
    path('api/inject/' , include('json_inject.urls')) ,
    path('ckeditor/' , include('ckeditor_uploader.urls')) ,

]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

# schema shit which does not work
# path('schema/' , get_schema_view(title='My Project' ,
#                                  description='a good API for a good frontend' ,
#                                  version='1.0' , ) ,
#      name='openapi-schema'
#      )
