from django import forms
from .models import Configuracion

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['nombre', 'lema', 'descripcion', 'email', 'telefono',
                  'direccion', 'horario', 'mensaje_landing', 'reservas_abiertas']
        labels = {
            'nombre': 'Nombre del ecoparque',
            'lema': 'Lema',
            'descripcion': 'Descripcion breve',
            'email': 'Correo de contacto',
            'telefono': 'Telefono',
            'direccion': 'Direccion',
            'horario': 'Horario de atencion',
            'mensaje_landing': 'Aviso en la pagina principal',
            'reservas_abiertas': 'Reservas abiertas al publico',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'mensaje_landing': forms.Textarea(attrs={'rows': 3}),
        }