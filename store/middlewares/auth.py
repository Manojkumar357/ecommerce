from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        # If the user is not logged in, redirect them to login page
        if not request.session.get('customer'):
            return redirect('login')
        # Otherwise, continue the request
        response = get_response(request)
        return response

    return middleware
