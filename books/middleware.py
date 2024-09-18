from .models import HttpRequestLog

class LogHttpRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = None

        HttpRequestLog.objects.create(
            path=request.path,
            method=request.method,
            user=user,
            remote_addr=request.META.get('REMOTE_ADDR')
        )

        return response
