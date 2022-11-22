from django.urls import path
from users.views import get_user


urlpatterns = [
    path('get_user/<int:id_user>/', get_user, name='get_user'),
]