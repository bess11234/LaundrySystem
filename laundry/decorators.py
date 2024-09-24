
from functools import wraps
from django.shortcuts import redirect

from django.core.exceptions import PermissionDenied
 
def is_role(role, user):
    try:
        if user.role == role:
            return True
    except AttributeError:
        return False
    return False
 
 
def access_only(role):
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not is_role(role, request.user):
                raise PermissionDenied("You don't have permission to access page.")
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator