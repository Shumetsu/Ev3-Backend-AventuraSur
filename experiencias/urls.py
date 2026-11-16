from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/nueva/', views.categoria_crear, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),
    path('', views.experiencia_lista, name='experiencia_lista'),
    path('nueva/', views.experiencia_crear, name='experiencia_crear'),
    path('<int:pk>/editar/', views.experiencia_editar, name='experiencia_editar'),
    path('<int:pk>/eliminar/', views.experiencia_eliminar, name='experiencia_eliminar'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('<int:pk>/inscribirse/', views.inscribirse, name='inscribirse'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('mis-reservas/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/', views.reserva_lista, name='reserva_lista'),
    path('reservas/<int:pk>/estado/', views.reserva_cambiar_estado, name='reserva_estado'),
    path('<int:pk>/', views.experiencia_detalle, name='experiencia_detalle'),
    path('<int:pk>/grupo/', views.experiencia_grupo, name='experiencia_grupo'),
    path('<int:pk>/estado/', views.experiencia_cambiar_estado, name='experiencia_estado'),
    path('<int:pk>/asistencia/', views.experiencia_asistencia, name='experiencia_asistencia'),
    path('mis-reservas/<int:pk>/valorar/', views.valorar, name='valorar'),
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/csv/', views.reportes_csv, name='reportes_csv'),
    path('calendario/', views.calendario, name='calendario'),
]