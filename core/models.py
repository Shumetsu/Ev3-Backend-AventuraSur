from django.db import models


class Configuracion(models.Model):
    """Configuracion general del sitio. Siempre existe una sola fila (pk=1)."""
    nombre = models.CharField(max_length=100, default='Aventuras del Sur')
    lema = models.CharField(max_length=200, blank=True,
                            default='Ecoparque y Reserva Natural')
    descripcion = models.TextField(
        blank=True, default='Reserva tu proxima experiencia al aire libre.')
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    horario = models.CharField(max_length=120, blank=True,
                               default='Lunes a domingo, 09:00 a 18:00')
    mensaje_landing = models.TextField(
        blank=True, help_text='Aviso que se muestra en la pagina principal. '
                              'Dejalo vacio para no mostrar ninguno.')
    reservas_abiertas = models.BooleanField(
        default=True, help_text='Si lo desmarcas, los turistas no podran inscribirse.')

    class Meta:
        verbose_name = 'Configuracion'
        verbose_name_plural = 'Configuracion'

    def save(self, *args, **kwargs):
        self.pk = 1  # fuerza una sola fila
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # no se elimina

    @classmethod
    def obtener(cls):
        config, _ = cls.objects.get_or_create(pk=1)
        return config

    def __str__(self):
        return self.nombre