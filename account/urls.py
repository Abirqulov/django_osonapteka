from .views import *
from django.urls import path


urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('user/<int:pk>', UserApiView.as_view(), name='user')

]
