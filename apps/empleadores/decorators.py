# empleadores/decorators.py
from functools import wraps
from django.http import JsonResponse

def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Debes iniciar sesión'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view