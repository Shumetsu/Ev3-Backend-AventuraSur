from django.contrib import messages
from django.db import transaction
from django.db.models import Avg, Count, F, ProtectedError, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse

from cuentas.decorators import rol_requerido
from .forms import CategoriaForm, ExperienciaForm, ValoracionForm
from .models import Categoria, Experiencia, Inscripcion, Valoracion
import csv
from datetime import datetime, time
from django.utils.dateparse import parse_date
import calendar
from core.models import Configuracion



@rol_requerido('administrador')
def categoria_lista(request):
    categorias = Categoria.objects.order_by('nombre')
    return render(request, 'experiencias/categoria_lista.html', {'categorias': categorias})


@rol_requerido('administrador')
def categoria_crear(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada correctamente.')
        return redirect('categoria_lista')
    return render(request, 'experiencias/categoria_form.html',
                  {'form': form, 'titulo': 'Nueva categoría'})


@rol_requerido('administrador')
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoría actualizada correctamente.')
        return redirect('categoria_lista')
    return render(request, 'experiencias/categoria_form.html',
                  {'form': form, 'titulo': 'Editar categoría'})


@rol_requerido('administrador')
@require_POST
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    try:
        categoria.delete()
        messages.success(request, 'Categoría eliminada.')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar: tiene experiencias asociadas. '
                                'Puedes desactivarla en su lugar.')
    return redirect('categoria_lista')

def _experiencias_visibles(user):
    """Admin ve todas; el guia solo las que creo."""
    qs = (Experiencia.objects
          .select_related('categoria', 'creador')
          .annotate(n_inscritos=Count('inscripciones')))
    if user.perfil.rol == 'guia':
        qs = qs.filter(creador=user)
    return qs.order_by('fecha_hora')


@rol_requerido('administrador', 'guia')
def experiencia_lista(request):
    return render(request, 'experiencias/experiencia_lista.html', {
        'experiencias': _experiencias_visibles(request.user),
        'es_admin': request.user.perfil.rol == 'administrador',
    })


@rol_requerido('administrador', 'guia')
def experiencia_crear(request):
    es_admin = request.user.perfil.rol == 'administrador'
    form = ExperienciaForm(request.POST or None, es_admin=es_admin, usuario=request.user)
    if request.method == 'POST' and form.is_valid():
        experiencia = form.save(commit=False)
        if not es_admin:
            experiencia.creador = request.user
        experiencia.save()
        messages.success(request, 'Experiencia creada correctamente.')
        return redirect('experiencia_lista')
    return render(request, 'experiencias/experiencia_form.html',
                  {'form': form, 'titulo': 'Nueva experiencia', 'es_admin': es_admin})


@rol_requerido('administrador', 'guia')
def experiencia_editar(request, pk):
    es_admin = request.user.perfil.rol == 'administrador'
    experiencia = get_object_or_404(_experiencias_visibles(request.user), pk=pk)
    form = ExperienciaForm(request.POST or None, instance=experiencia,
                           es_admin=es_admin, usuario=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Experiencia actualizada correctamente.')
        return redirect('experiencia_lista')
    return render(request, 'experiencias/experiencia_form.html',
                  {'form': form, 'titulo': 'Editar experiencia', 'es_admin': es_admin})


@rol_requerido('administrador')
@require_POST
def experiencia_eliminar(request, pk):
    experiencia = get_object_or_404(Experiencia, pk=pk)
    experiencia.delete()
    messages.success(request, 'Experiencia eliminada.')
    return redirect('experiencia_lista')

@rol_requerido('turista')
def catalogo(request):
    experiencias = (Experiencia.objects
                    .filter(activo=True, categoria__activo=True, estado_ruta=Experiencia.PROGRAMADA, fecha_hora__gte=timezone.now())
                    .select_related('categoria')
                    .annotate(n_inscritos=Count('inscripciones'))
                    .annotate(cupos=F('cupo_maximo') - F('n_inscritos'))
                    .order_by('fecha_hora'))
    inscritas = set(Inscripcion.objects
                    .filter(usuario=request.user)
                    .values_list('experiencia_id', flat=True))
    return render(request, 'experiencias/catalogo.html',
                  {'experiencias': experiencias, 'inscritas': inscritas})


@rol_requerido('turista')
@require_POST
def inscribirse(request, pk):
    with transaction.atomic():
        if not Configuracion.obtener().reservas_abiertas:
            messages.error(request, 'Las reservas estan cerradas temporalmente.')
            return redirect('catalogo')
        experiencia = get_object_or_404(Experiencia.objects.select_for_update(), pk=pk)

        if (not experiencia.activo or not experiencia.categoria.activo
                or experiencia.estado_ruta != Experiencia.PROGRAMADA
                or experiencia.fecha_hora < timezone.now()):
            messages.error(request, 'Esta experiencia ya no esta disponible.')
            return redirect('catalogo')

        if Inscripcion.objects.filter(usuario=request.user, experiencia=experiencia).exists():
            messages.warning(request, 'Ya estas inscrito en esta experiencia.')
            return redirect('mis_reservas')

        if experiencia.inscripciones.count() >= experiencia.cupo_maximo:
            messages.error(request, 'No quedan cupos disponibles.')
            return redirect('catalogo')

        Inscripcion.objects.create(usuario=request.user, experiencia=experiencia)

    messages.success(request, f'Te inscribiste en "{experiencia.titulo}". El pago queda pendiente.')
    return redirect('mis_reservas')


@rol_requerido('turista')
def mis_reservas(request):
    reservas = (Inscripcion.objects
                .filter(usuario=request.user)
                .select_related('experiencia__categoria', 'valoracion')
                .order_by('-fecha_inscripcion'))
    return render(request, 'experiencias/mis_reservas.html', {'reservas': reservas})


@rol_requerido('turista')
@require_POST
def cancelar_reserva(request, pk):
    # Filtrar por usuario impide cancelar reservas de otros turistas
    reserva = get_object_or_404(Inscripcion, pk=pk, usuario=request.user)
    if reserva.estado_pago != Inscripcion.PENDIENTE:
        messages.error(request, 'Solo puedes cancelar reservas con pago pendiente.')
    else:
        reserva.delete()
        messages.success(request, 'Reserva cancelada.')
    return redirect('mis_reservas')

@rol_requerido('administrador')
def reserva_lista(request):
    reservas = (Inscripcion.objects
                .select_related('usuario', 'experiencia__categoria')
                .order_by('-fecha_inscripcion'))
    return render(request, 'experiencias/reserva_lista.html', {'reservas': reservas})


@rol_requerido('administrador')
@require_POST
def reserva_cambiar_estado(request, pk):
    reserva = get_object_or_404(Inscripcion, pk=pk)
    if reserva.estado_pago == Inscripcion.CONFIRMADO:
        reserva.estado_pago = Inscripcion.PENDIENTE
    else:
        reserva.estado_pago = Inscripcion.CONFIRMADO
    reserva.save(update_fields=['estado_pago'])
    messages.success(request, f'Pago marcado como {reserva.get_estado_pago_display().lower()}.')
    return redirect('reserva_lista')

@rol_requerido('turista')
def experiencia_detalle(request, pk):
    experiencia = get_object_or_404(
        Experiencia.objects.select_related('categoria', 'creador'), pk=pk)
    mi_reserva = Inscripcion.objects.filter(
        usuario=request.user, experiencia=experiencia).first()
    disponible = experiencia.activo and experiencia.categoria.activo

    if not disponible and not mi_reserva:
        raise Http404

    cupos = experiencia.cupos_disponibles
    ya_paso = experiencia.fecha_hora < timezone.now()

    valoraciones = (Valoracion.objects
                    .filter(inscripcion__experiencia=experiencia)
                    .select_related('inscripcion__usuario')
                    .order_by('-fecha'))
    resumen = valoraciones.aggregate(promedio=Avg('puntaje'), total=Count('id'))
    puede_valorar = bool(mi_reserva and mi_reserva.asistio
                         and experiencia.estado_ruta == Experiencia.FINALIZADA)
    mi_valoracion = valoraciones.filter(inscripcion=mi_reserva).first() if mi_reserva else None

    return render(request, 'experiencias/experiencia_detalle.html', {
        'e': experiencia,
        'reserva': mi_reserva,
        'cupos': cupos,
        'ya_paso': ya_paso,
        'puede_inscribirse': (disponible and not ya_paso and cupos > 0 and not mi_reserva
                                and experiencia.estado_ruta == Experiencia.PROGRAMADA
                                and Configuracion.obtener().reservas_abiertas),
        'valoraciones': valoraciones,
        'resumen': resumen,
        'puede_valorar': puede_valorar,
        'mi_valoracion': mi_valoracion,
    })

TRANSICIONES = {
    Experiencia.PROGRAMADA: [Experiencia.EN_CURSO, Experiencia.CANCELADA],
    Experiencia.EN_CURSO: [Experiencia.FINALIZADA, Experiencia.CANCELADA],
    Experiencia.FINALIZADA: [],
    Experiencia.CANCELADA: [],
}
ETIQUETAS_ESTADO = {
    Experiencia.EN_CURSO: 'Iniciar ruta',
    Experiencia.FINALIZADA: 'Finalizar ruta',
    Experiencia.CANCELADA: 'Cancelar ruta',
}
    
@rol_requerido('administrador', 'guia')
def experiencia_grupo(request, pk):
    experiencia = get_object_or_404(_experiencias_visibles(request.user), pk=pk)
    inscritos = (experiencia.inscripciones
                 .select_related('usuario__perfil')
                 .order_by('usuario__first_name', 'usuario__last_name'))
    confirmados = inscritos.filter(estado_pago=Inscripcion.CONFIRMADO).count()
    acciones = [(est, ETIQUETAS_ESTADO[est]) for est in TRANSICIONES[experiencia.estado_ruta]]
    valoraciones = (Valoracion.objects
                    .filter(inscripcion__experiencia=experiencia)
                    .select_related('inscripcion__usuario')
                    .order_by('-fecha'))
    resumen = valoraciones.aggregate(promedio=Avg('puntaje'), total=Count('id'))
    return render(request, 'experiencias/experiencia_grupo.html', {
        'e': experiencia,
        'inscritos': inscritos,
        'total': experiencia.n_inscritos,
        'confirmados': confirmados,
        'pendientes': experiencia.n_inscritos - confirmados,
        'asistentes': inscritos.filter(asistio=True).count(),
        'acciones': acciones,
        'puede_asistencia': experiencia.estado_ruta in (Experiencia.EN_CURSO, Experiencia.FINALIZADA),
        'valoraciones': valoraciones,
        'resumen': resumen,
    })


@rol_requerido('administrador', 'guia')
@require_POST
def experiencia_cambiar_estado(request, pk):
    experiencia = get_object_or_404(_experiencias_visibles(request.user), pk=pk)
    nuevo = request.POST.get('estado')
    if nuevo in TRANSICIONES[experiencia.estado_ruta]:
        experiencia.estado_ruta = nuevo
        experiencia.save(update_fields=['estado_ruta'])
        messages.success(request, f'Ruta {experiencia.get_estado_ruta_display().lower()}.')
    else:
        messages.error(request, 'Ese cambio de estado no es valido.')
    return redirect('experiencia_grupo', pk=pk)


@rol_requerido('administrador', 'guia')
@require_POST
def experiencia_asistencia(request, pk):
    experiencia = get_object_or_404(_experiencias_visibles(request.user), pk=pk)
    if experiencia.estado_ruta not in (Experiencia.EN_CURSO, Experiencia.FINALIZADA):
        messages.error(request, 'Solo puedes registrar asistencia con la ruta en curso o finalizada.')
        return redirect('experiencia_grupo', pk=pk)
    ids = [int(x) for x in request.POST.getlist('asistio') if x.isdigit()]
    with transaction.atomic():
        experiencia.inscripciones.update(asistio=False)
        experiencia.inscripciones.filter(pk__in=ids).update(asistio=True)
    messages.success(request, 'Asistencia guardada.')
    return redirect('experiencia_grupo', pk=pk)

@rol_requerido('turista')
def valorar(request, pk):
    # pk es el de la inscripcion; filtrar por usuario impide valorar reservas ajenas
    inscripcion = get_object_or_404(
        Inscripcion.objects.select_related('experiencia'), pk=pk, usuario=request.user)
    experiencia = inscripcion.experiencia

    if not (inscripcion.asistio and experiencia.estado_ruta == Experiencia.FINALIZADA):
        messages.error(request, 'Solo puedes valorar experiencias a las que asististe '
                                'y que ya finalizaron.')
        return redirect('mis_reservas')

    valoracion = Valoracion.objects.filter(inscripcion=inscripcion).first()
    form = ValoracionForm(request.POST or None, instance=valoracion)
    if request.method == 'POST' and form.is_valid():
        nueva = form.save(commit=False)
        nueva.inscripcion = inscripcion
        nueva.save()
        messages.success(request, 'Gracias por tu valoracion.')
        return redirect('experiencia_detalle', pk=experiencia.pk)

    return render(request, 'experiencias/valorar.html', {
        'form': form,
        'e': experiencia,
        'valores': [5, 4, 3, 2, 1],
        'editando': valoracion is not None,
    })

def _fecha(valor):
    try:
        return parse_date(valor or '')
    except ValueError:
        return None


def _datos_reporte(request):
    """Calcula una fila por experiencia, aplicando el filtro de fechas si viene."""
    desde = _fecha(request.GET.get('desde'))
    hasta = _fecha(request.GET.get('hasta'))

    base = Experiencia.objects.all()
    if desde:
        base = base.filter(fecha_hora__gte=timezone.make_aware(datetime.combine(desde, time.min)))
    if hasta:
        base = base.filter(fecha_hora__lte=timezone.make_aware(datetime.combine(hasta, time.max)))

    consulta = (base.select_related('categoria')
                .annotate(
                    n_inscritos=Count('inscripciones', distinct=True),
                    n_confirmados=Count('inscripciones', distinct=True,
                                        filter=Q(inscripciones__estado_pago=Inscripcion.CONFIRMADO)),
                    n_asistentes=Count('inscripciones', distinct=True,
                                       filter=Q(inscripciones__asistio=True)),
                    n_valoraciones=Count('inscripciones__valoracion', distinct=True),
                    promedio=Avg('inscripciones__valoracion__puntaje'))
                .order_by('fecha_hora'))

    filas = []
    for e in consulta:
        precio = int(e.precio)
        filas.append({
            'titulo': e.titulo,
            'categoria': e.categoria.nombre,
            'fecha': e.fecha_hora,
            'ruta': e.get_estado_ruta_display(),
            'precio': precio,
            'cupo': e.cupo_maximo,
            'inscritos': e.n_inscritos,
            'confirmados': e.n_confirmados,
            'asistentes': e.n_asistentes,
            'ocupacion': round(100 * e.n_inscritos / e.cupo_maximo) if e.cupo_maximo else 0,
            'ingresos': precio * e.n_confirmados,
            'pendiente': precio * (e.n_inscritos - e.n_confirmados),
            'promedio': round(float(e.promedio), 1) if e.promedio is not None else None,
            'n_val': e.n_valoraciones,
        })
    return {'desde': desde, 'hasta': hasta, 'base': base, 'filas': filas}


@rol_requerido('administrador')
def reportes(request):
    d = _datos_reporte(request)
    filas = d['filas']

    total_ins = sum(f['inscritos'] for f in filas)
    total_conf = sum(f['confirmados'] for f in filas)
    total_cupo = sum(f['cupo'] for f in filas)

    val = (Valoracion.objects
           .filter(inscripcion__experiencia__in=d['base'])
           .aggregate(prom=Avg('puntaje'), total=Count('id')))
    turistas = (Inscripcion.objects
                .filter(experiencia__in=d['base'])
                .values('usuario').distinct().count())

    por_categoria, por_ruta = {}, {}
    for f in filas:
        por_categoria[f['categoria']] = por_categoria.get(f['categoria'], 0) + f['ingresos']
        por_ruta[f['ruta']] = por_ruta.get(f['ruta'], 0) + 1

    resumen = {
        'ingresos_conf': sum(f['ingresos'] for f in filas),
        'ingresos_pend': sum(f['pendiente'] for f in filas),
        'reservas': total_ins,
        'confirmadas': total_conf,
        'pendientes': total_ins - total_conf,
        'ocupacion': round(100 * total_ins / total_cupo) if total_cupo else 0,
        'turistas': turistas,
        'promedio': round(float(val['prom']), 1) if val['prom'] is not None else None,
        'n_valoraciones': val['total'],
        'n_experiencias': len(filas),
    }
    datos = {
        'estado': {'labels': ['Confirmadas', 'Pendientes'],
                   'valores': [total_conf, total_ins - total_conf]},
        'ocupacion': {'labels': [f['titulo'] for f in filas],
                      'valores': [f['ocupacion'] for f in filas]},
        'categorias': {'labels': list(por_categoria.keys()),
                       'valores': list(por_categoria.values())},
        'ruta': {'labels': list(por_ruta.keys()),
                 'valores': list(por_ruta.values())},
    }
    return render(request, 'experiencias/reportes.html', {
        'desde': d['desde'], 'hasta': d['hasta'],
        'filas': filas, 'resumen': resumen, 'datos': datos,
    })


@rol_requerido('administrador')
def reportes_csv(request):
    filas = _datos_reporte(request)['filas']
    respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
    respuesta['Content-Disposition'] = 'attachment; filename="reporte_experiencias.csv"'
    respuesta.write('\ufeff')  # marca BOM para que Excel lea bien las tildes
    escritor = csv.writer(respuesta, delimiter=';')
    escritor.writerow(['Experiencia', 'Categoria', 'Fecha', 'Ruta', 'Precio', 'Cupo',
                       'Inscritos', 'Confirmados', 'Asistentes', 'Ocupacion %',
                       'Ingresos confirmados', 'Ingresos pendientes',
                       'Valoracion promedio', 'N valoraciones'])
    for f in filas:
        escritor.writerow([
            f['titulo'], f['categoria'],
            timezone.localtime(f['fecha']).strftime('%d/%m/%Y %H:%M'),
            f['ruta'], f['precio'], f['cupo'], f['inscritos'], f['confirmados'],
            f['asistentes'], f['ocupacion'], f['ingresos'], f['pendiente'],
            str(f['promedio']).replace('.', ',') if f['promedio'] is not None else '',
            f['n_val'],
        ])
    return respuesta

NOMBRE_MES = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
              'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
COLOR_RUTA = {
    Experiencia.PROGRAMADA: 'info',
    Experiencia.EN_CURSO: 'warning',
    Experiencia.FINALIZADA: 'success',
    Experiencia.CANCELADA: 'danger',
}


@rol_requerido('administrador', 'guia')
def calendario(request):
    hoy = timezone.localdate()
    try:
        anio = int(request.GET.get('anio', hoy.year))
        mes = int(request.GET.get('mes', hoy.month))
        if not 1 <= mes <= 12 or not 2000 <= anio <= 2100:
            raise ValueError
    except (TypeError, ValueError):
        anio, mes = hoy.year, hoy.month

    ant_anio, ant_mes = (anio - 1, 12) if mes == 1 else (anio, mes - 1)
    sig_anio, sig_mes = (anio + 1, 1) if mes == 12 else (anio, mes + 1)

    # Rango [primer dia del mes, primer dia del mes siguiente)
    inicio = timezone.make_aware(datetime(anio, mes, 1))
    fin = timezone.make_aware(datetime(sig_anio, sig_mes, 1))
    delmes = _experiencias_visibles(request.user).filter(
        fecha_hora__gte=inicio, fecha_hora__lt=fin)

    # Agrupa las experiencias por dia del mes
    por_dia = {}
    for e in delmes:
        dia = timezone.localtime(e.fecha_hora).day
        por_dia.setdefault(dia, []).append({
            'obj': e,
            'hora': timezone.localtime(e.fecha_hora).strftime('%H:%M'),
            'color': COLOR_RUTA[e.estado_ruta],
        })

    cal = calendar.Calendar(firstweekday=0)  # 0 = lunes
    semanas = []
    for semana in cal.monthdayscalendar(anio, mes):
        fila = []
        for dia in semana:
            fila.append({
                'dia': dia,
                'hoy': dia and anio == hoy.year and mes == hoy.month and dia == hoy.day,
                'items': por_dia.get(dia, []),
            })
        semanas.append(fila)

    ant_anio, ant_mes = (anio - 1, 12) if mes == 1 else (anio, mes - 1)
    sig_anio, sig_mes = (anio + 1, 1) if mes == 12 else (anio, mes + 1)

    proximas = (_experiencias_visibles(request.user)
                .filter(fecha_hora__gte=timezone.now())
                .exclude(estado_ruta=Experiencia.CANCELADA)[:5])

    return render(request, 'experiencias/calendario.html', {
        'semanas': semanas,
        'anio': anio, 'mes': mes, 'nombre_mes': NOMBRE_MES[mes],
        'ant': {'anio': ant_anio, 'mes': ant_mes},
        'sig': {'anio': sig_anio, 'mes': sig_mes},
        'hoy': hoy,
        'del_mes': delmes.order_by('fecha_hora'),
        'proximas': proximas,
        'es_admin': request.user.perfil.rol == 'administrador',
    })

