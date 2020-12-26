from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import sample_list_view , CpuListView , SampleViewSet , CategoryViewSet , GenreViewSet , BandView

router = DefaultRouter()
router.register('sample' , SampleViewSet , basename='sample')
router.register('cat' , CategoryViewSet , basename='category')
router.register('genre' , GenreViewSet , basename='genre')
urlpatterns = router.urls

# app_name = 'inject'
#
urlpatterns += [
    # path('cpu/' , CpuListView.as_view()) ,
    # path('<int:pk>/' , sample_detail_view)
    # path('genre/' , sample_detail_view)
    path('gg/<slug:slug1>/<slug:slug2>/<int:pk>/' , BandView.as_view())

]
