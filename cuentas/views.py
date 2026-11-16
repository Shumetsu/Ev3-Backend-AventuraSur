from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Perfil

from .decorators import rol_requerido
from .forms import RegistroForm, UsuarioCrearForm, UsuarioEditarForm, PerfilForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Cuenta creada. ¡Bienvenido!')
        return redirect('dashboard')
    return render(request, 'cuentas/registro.html', {'form': form})

@rol_requerido('administrador')
def usuario_lista(request):
    usuarios = User.objects.select_related('perfil').order_by('username')
    return render(request, 'cuentas/usuario_lista.html', {'usuarios': usuarios})


@rol_requerido('administrador')
def usuario_crear(request):
    form = UsuarioCrearForm(request.POST or None, initial={'rol': request.GET.get('rol', Perfil.TURISTA)})
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente.')
        return redirect('usuario_lista')
    return render(request, 'cuentas/usuario_form.html',
                  {'form': form, 'titulo': 'Nuevo usuario'})


@rol_requerido('administrador')
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = UsuarioEditarForm(request.POST or None, instance=usuario,
                             es_propio=(usuario == request.user))
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('usuario_lista')
    return render(request, 'cuentas/usuario_form.html',
                  {'form': form, 'titulo': 'Editar usuario', 'editando': True})


@rol_requerido('administrador')
@require_POST
def usuario_cambiar_estado(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
    else:
        usuario.is_active = not usuario.is_active
        usuario.save(update_fields=['is_active'])
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Usuario {usuario.username} {estado}.')
    return redirect('usuario_lista')

@login_required
def perfil(request):
    form = PerfilForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('perfil')
    return render(request, 'cuentas/perfil.html', {'form': form})


class PasswordCambiarView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'cuentas/password_cambiar.html'
    success_url = reverse_lazy('perfil')
    success_message = 'Contrasena actualizada correctamente.'
    
@rol_requerido('administrador')
def guia_lista(request):
    guias = (User.objects.filter(perfil__rol=Perfil.GUIA)
             .select_related('perfil')
             .annotate(n_experiencias=Count('experiencias_creadas', distinct=True),
                       n_inscritos=Count('experiencias_creadas__inscripciones', distinct=True))
             .order_by('first_name', 'username'))
    return render(request, 'cuentas/guia_lista.html', {'guias': guias})