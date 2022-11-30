from django.shortcuts import redirect
from django.conf import settings


class LoginMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = '.'.join((view_func.__module__, view_func.__name__))
        exclusion_set = settings.EXCLUDE_FROM_MY_MIDDLEWARE
        if view_name in exclusion_set:
            return None
        if request.user.is_authenticated:
            return None
        return redirect(settings.LOGIN_URL)
