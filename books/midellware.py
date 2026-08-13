#tarin middleware

def my_middleware(get_response):
    def middleware(request):
        print("Before view")
        print(request.META.get('HTTP_USER_AGENT'))
        response = get_response(request)
        print(response.status_code)
        print("After view")

        return response

    return middleware










