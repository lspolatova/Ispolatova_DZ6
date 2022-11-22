from django.http import JsonResponse
from users.models import User
from django.views.decorators.http import require_GET


@require_GET
def get_user(request, id_user):
    """
    get user information by id
    """
    user = list(User.objects.filter(id=id_user).values())
    return JsonResponse(user, safe=False)
