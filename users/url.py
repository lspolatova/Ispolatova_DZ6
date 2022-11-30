from django.urls import path
from users.views import GetUser


urlpatterns = [
    path('get/<int:pk>', GetUser.as_view(), name='get'),
]
