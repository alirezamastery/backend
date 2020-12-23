from django.urls import path , include

from .views import sample_list_view , sample_detail_view

app_name = 'inject'

urlpatterns = [
    path('' , sample_list_view) ,
    path('<int:pk>/' , sample_detail_view)
]
