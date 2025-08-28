from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Chech User is Authenticated
        if request.user.is_authenticated:
            # List of Paths to Check
            path_to_redirect = [reverse('accounts:login_page'), reverse('accounts:register_page')]

            if request.path in path_to_redirect:
                return redirect(reverse('abdellah_shoping:home_page'))
            
        response = self.get_response(request)
        return response
    
class RestrictUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_path = [reverse('accounts:dashboard_page')]

        if not request.user.is_authenticated and request.path in restricted_path:
            return redirect(reverse('accounts:login_page'))
        
        response = self.get_response(request)
        return response
