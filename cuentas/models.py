from django.db import models
from django.conf import settings

class Perfil(models.Model):
    ADMINISTRADOR = 'administrador'
    GUIA = 'guia'
    TURISTA = 'turista'
    ROLES = [
        (ADMINISTRADOR, 'Administrador'),
        (GUIA, 'Guia / Operador'),
        (TURISTA, 'Turista / Cliente'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil'
    )
    rol = models.CharField(max_length=20, choices=ROLES, default=TURISTA)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.usuario.username} ({self.get_rol_display()})'
