from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from cuentas.models import Perfil
from experiencias.models import Categoria, Experiencia, Inscripcion

CLAVE = 'Aventura2026!'

# username, nombre, apellido, rol
USUARIOS = [
    ('admin', 'Andrea', 'Fuentes', Perfil.ADMINISTRADOR),
    ('guia1', 'Camila', 'Rojas', Perfil.GUIA),
    ('guia2', 'Matias', 'Soto', Perfil.GUIA),
    ('turista1', 'Valentina', 'Perez', Perfil.TURISTA),
    ('turista2', 'Diego', 'Munoz', Perfil.TURISTA),
]

CATEGORIAS = [
    ('Trekking', 'Caminatas guiadas por los senderos de la reserva.'),
    ('Canopy', 'Circuitos de tirolesas entre los arboles.'),
    ('Kayak', 'Paseos en kayak por aguas tranquilas.'),
    ('Arriendo de equipos', 'Equipamiento para actividades al aire libre.'),
]

# guia, titulo, descripcion, categoria, precio, cupo, dias desde hoy
EXPERIENCIAS = [
    ('guia1', 'Kayak al amanecer', 'Paseo en kayak mientras sale el sol sobre el lago.', 'Kayak', 25000, 2, 5),
    ('guia1', 'Trekking Sendero del Bosque', 'Caminata de 4 horas por el bosque nativo.', 'Trekking', 15000, 12, 8),
    ('guia1', 'Canopy Alto', 'Circuito de 8 tirolesas sobre el valle.', 'Canopy', 30000, 10, 12),
    ('guia1', 'Arriendo de equipo de camping', 'Carpa, saco de dormir y cocinilla por un fin de semana.', 'Arriendo de equipos', 12000, 20, 15),
    ('guia2', 'Trekking a la Cascada', 'Ruta guiada hasta la cascada de la reserva.', 'Trekking', 18000, 15, 6),
    ('guia2', 'Kayak en el Lago', 'Recorrido tranquilo para toda la familia.', 'Kayak', 22000, 8, 10),
    ('guia2', 'Canopy Nocturno', 'Tirolesas con iluminacion especial al atardecer.', 'Canopy', 35000, 6, 14),
    ('guia2', 'Arriendo de bicicletas', 'Bicicletas de montana por el dia, con casco.', 'Arriendo de equipos', 10000, 15, 20),
]

# turista, titulo de la experiencia, estado de pago
INSCRIPCIONES = [
    ('turista1', 'Kayak al amanecer', Inscripcion.CONFIRMADO),
    ('turista1', 'Trekking Sendero del Bosque', Inscripcion.PENDIENTE),
    ('turista1', 'Trekking a la Cascada', Inscripcion.PENDIENTE),
    ('turista1', 'Canopy Nocturno', Inscripcion.CONFIRMADO),
    ('turista2', 'Kayak al amanecer', Inscripcion.PENDIENTE),
    ('turista2', 'Canopy Alto', Inscripcion.CONFIRMADO),
    ('turista2', 'Trekking a la Cascada', Inscripcion.PENDIENTE),
    ('turista2', 'Kayak en el Lago', Inscripcion.PENDIENTE),
]


class Command(BaseCommand):
    help = 'Carga usuarios, categorias, experiencias e inscripciones de prueba.'

    @transaction.atomic
    def handle(self, *args, **options):
        usuarios = {}
        for username, nombre, apellido, rol in USUARIOS:
            user = User.objects.filter(username=username).first()
            if not user:
                correo = f'{username}@aventurasdelsur.cl'
                if rol == Perfil.ADMINISTRADOR:
                    user = User.objects.create_superuser(
                        username, correo, CLAVE, first_name=nombre, last_name=apellido)
                else:
                    user = User.objects.create_user(
                        username, correo, CLAVE, first_name=nombre, last_name=apellido)
            perfil, _ = Perfil.objects.get_or_create(usuario=user)
            perfil.rol = rol
            perfil.save()
            usuarios[username] = user

        categorias = {}
        for nombre, descripcion in CATEGORIAS:
            cat, _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={'descripcion': descripcion})
            categorias[nombre] = cat

        experiencias = {}
        for guia, titulo, descripcion, cat, precio, cupo, dias in EXPERIENCIAS:
            fecha = (timezone.now() + timedelta(days=dias)).replace(
                hour=10, minute=0, second=0, microsecond=0)
            exp, _ = Experiencia.objects.get_or_create(
                titulo=titulo, creador=usuarios[guia],
                defaults={'descripcion': descripcion, 'categoria': categorias[cat],
                          'precio': precio, 'cupo_maximo': cupo, 'fecha_hora': fecha})
            experiencias[titulo] = exp

        for turista, titulo, estado in INSCRIPCIONES:
            Inscripcion.objects.get_or_create(
                usuario=usuarios[turista], experiencia=experiencias[titulo],
                defaults={'estado_pago': estado})

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {len(usuarios)} usuarios, {len(categorias)} categorias, '
            f'{len(experiencias)} experiencias, {len(INSCRIPCIONES)} inscripciones.'))