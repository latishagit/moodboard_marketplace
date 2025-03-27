from django.core.exceptions import PermissionDenied

def creator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.role=='creator':
            raise PermissionDenied  # Block unauthorized users
        return view_func(request, *args, **kwargs)
    return wrapper

def buyer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.role=='buyer':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

