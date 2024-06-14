from django.middleware.csrf import get_token


class HttpMethodOverrideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("!!!!!!!!!!!! - midlware")
        if request.method == "POST" and "_method" in request.POST:
            print("!!!! - mehod POST")
            print(f"request.POST: {request.POST}")

            # print(f"request.DELETE: {request.DELETE}")
            request.method = request.POST["_method"].upper()
            # csrf_token = get_token(request)
            # request.META["X-CSRFToken"] = csrf_token
            print(f"!!!!! new methot: {request.method}")
            # request.DELETE = request.POST
            
        response = self.get_response(request)

        # return self.get_response(request)
        return response


