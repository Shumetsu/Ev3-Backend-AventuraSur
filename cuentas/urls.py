from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('usuarios/', views.usuario_lista, name='usuario_lista'),
    path('usuarios/nuevo/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:pk>/editar/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/<int:pk>/estado/', views.usuario_cambiar_estado, name='usuario_estado'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/password/', views.PasswordCambiarView.as_view(), name='password_cambiar'),
    path('guias/', views.guia_lista, name='guia_lista'),
]