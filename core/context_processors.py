from .models import Configuracion


def configuracion(request):
    return {'config': Configuracion.obtener()}