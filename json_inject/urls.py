from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import sample_list_view , sample_detail_view , SampleViewSet

router = DefaultRouter()
router.register('' , SampleViewSet , basename='sample')
urlpatterns = router.urls

# app_name = 'inject'
#
# urlpatterns = [
#     path('' , sample_list_view) ,
#     path('<int:pk>/' , sample_detail_view)
# ]
