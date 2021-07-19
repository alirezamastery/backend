from django.urls import path
from .views import (register,
                    UserLogin,
                    UserLogout,
                    CustomUserCreate,
                    BlacklistTokenUpdateView,
                    UserDetailView
                    )


app_name = 'users'

urlpatterns = [
    # path('register/' , CustomUserCreate.as_view() , name='user-register') ,
    path('register/', register, name='user-register'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist')
]
