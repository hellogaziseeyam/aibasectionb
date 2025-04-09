from django.http import HttpResponseForbidden

def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")
            if hasattr(request.user, 'profile') and request.user.profile.role == required_role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don’t have permission to access this page.")
        return wrapper
    return decorator
