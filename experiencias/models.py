from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cupo_maximo = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField()
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='experiencias'
    )
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='experiencias_creadas'
    )
    
    PROGRAMADA = 'programada'
    EN_CURSO = 'en_curso'
    FINALIZADA = 'finalizada'
    CANCELADA = 'cancelada'
    ESTADOS_RUTA = [
        (PROGRAMADA, 'Programada'),
        (EN_CURSO, 'En curso'),
        (FINALIZADA, 'Finalizada'),
        (CANCELADA, 'Cancelada'),
    ]
    estado_ruta = models.CharField(max_length=20, choices=ESTADOS_RUTA, default=PROGRAMADA)

    def __str__(self):
        return self.titulo

    @property
    def cupos_disponibles(self):
        return self.cupo_maximo - self.inscripciones.count()


class Inscripcion(models.Model):
    PENDIENTE = 'pendiente'
    CONFIRMADO = 'confirmado'
    ESTADOS_PAGO = [
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADO, 'Confirmado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscripciones'
    )
    experiencia = models.ForeignKey(
        Experiencia, on_delete=models.CASCADE, related_name='inscripciones'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default=PENDIENTE)
    asistio = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'experiencia')

    def __str__(self):
        return f'{self.usuario.username} → {self.experiencia.titulo}'

class Valoracion(models.Model):
    # OneToOne con Inscripcion: garantiza una sola valoracion por turista y experiencia
    inscripcion = models.OneToOneField(
        Inscripcion, on_delete=models.CASCADE, related_name='valoracion'
    )
    puntaje = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    @property
    def estrellas(self):
        return '★' * self.puntaje + '☆' * (5 - self.puntaje)

    def __str__(self):
        return f'{self.inscripcion} ({self.puntaje}/5)'