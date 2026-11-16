from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def rol_requerido(*roles):
    def decorador(vista):
        @wraps(vista)
        @login_required
        def envoltura(request, *args, **kwargs):
            if request.user.perfil.rol not in roles:
                raise PermissionDenied  #Responde 403
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador