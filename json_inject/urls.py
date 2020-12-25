from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import sample_list_view , CpuListView , SampleViewSet , CategoryViewSet

router = DefaultRouter()
router.register('sample' , SampleViewSet , basename='sample')
router.register('cat' , CategoryViewSet , basename='category')
urlpatterns = router.urls

# app_name = 'inject'
#
urlpatterns += [
    # path('cpu/' , CpuListView.as_view()) ,
    # path('<int:pk>/' , sample_detail_view)
]
