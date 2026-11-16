from django import forms
from django.db.models import Q
from django.utils import timezone
from .models import Categoria, Experiencia, Valoracion

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        labels = {'nombre': 'Nombre', 'descripcion': 'Descripcion', 'activo': 'Categoria activa'}
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}
        
class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['titulo', 'descripcion', 'categoria', 'precio',
                  'cupo_maximo', 'fecha_hora', 'activo']
        labels = {
            'titulo': 'Titulo',
            'descripcion': 'Descripcion',
            'categoria': 'Categoria',
            'precio': 'Precio (CLP)',
            'cupo_maximo': 'Cupo maximo',
            'fecha_hora': 'Fecha y hora',
            'activo': 'Experiencia activa (visible para turistas)',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'precio': forms.NumberInput(attrs={'min': 0}),
            'cupo_maximo': forms.NumberInput(attrs={'min': 1}),
            'fecha_hora': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_hora'].input_formats = ['%Y-%m-%dT%H:%M']

        filtro = Q(activo=True)
        if self.instance.pk:
            filtro |= Q(pk=self.instance.categoria_id)
        self.fields['categoria'].queryset = Categoria.objects.filter(filtro)

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_cupo_maximo(self):
        cupo = self.cleaned_data['cupo_maximo']
        if cupo < 1:
            raise forms.ValidationError('El cupo debe ser al menos 1.')
        if self.instance.pk and cupo < self.instance.inscripciones.count():
            raise forms.ValidationError(
                'El cupo no puede ser menor a las inscripciones ya existentes '
                f'({self.instance.inscripciones.count()}).')
        return cupo

    def clean_fecha_hora(self):
        fecha = self.cleaned_data['fecha_hora']
        if not self.instance.pk and fecha < timezone.now():
            raise forms.ValidationError('La fecha debe ser futura.')
        return fecha

class ValoracionForm(forms.ModelForm):
    puntaje = forms.TypedChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)], coerce=int,
        error_messages={'required': 'Elige un puntaje de 1 a 5.'},
    )

    class Meta:
        model = Valoracion
        fields = ['puntaje', 'comentario']
        labels = {'comentario': 'Comentario (opcional)'}
        widgets = {'comentario': forms.Textarea(attrs={'rows': 4})}