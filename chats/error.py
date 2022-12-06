from django.http import JsonResponse


def error_not_get(func):
    def inner_function(request, id = None):
        if request.method != "GET":
            return JsonResponse({'error': '405'}, status=405)
        return func(request, id)
    return inner_function


def error_not_post(func):
    def inner_function(request):
        if request.method != "POST":
            return JsonResponse({'error': '405'}, status=405)
        return func(request)
    return inner_function
