from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from cuentas.decorators import rol_requerido
from .forms import ConfiguracionForm
from .models import Configuracion

def home(request):
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@rol_requerido('administrador')
def configuracion(request):
    config = Configuracion.obtener()
    form = ConfiguracionForm(request.POST or None, instance=config)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Configuracion guardada correctamente.')
        return redirect('configuracion')
    return render(request, 'core/configuracion.html', {'form': form})