
from functools import wraps
from django.shortcuts import redirect
 
 
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
                return redirect("index")
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator