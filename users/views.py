from rest_framework.generics import RetrieveAPIView

from users.models import User
from users.serializer import UserSerializer


class GetUser(RetrieveAPIView):
    """
    get user information by id
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
