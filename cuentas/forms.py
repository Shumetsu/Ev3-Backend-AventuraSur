from .models import Perfil
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  # la señal crea el Perfil como turista
            user.perfil.telefono = self.cleaned_data['telefono']
            user.perfil.save()
        return user

class UsuarioCrearForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo')
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol')
    telefono = forms.CharField(max_length=20, required=False, label='Telefono')

    field_order = ['username', 'first_name', 'last_name', 'email',
                   'rol', 'telefono', 'password1', 'password2']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {'username': 'Usuario', 'first_name': 'Nombre', 'last_name': 'Apellido'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  # la senal crea el Perfil
            perfil = user.perfil
            perfil.rol = self.cleaned_data['rol']
            perfil.telefono = self.cleaned_data['telefono']
            perfil.save()
        return user


class UsuarioEditarForm(forms.ModelForm):
    rol = forms.ChoiceField(choices=Perfil.ROLES, label='Rol')
    telefono = forms.CharField(max_length=20, required=False, label='Telefono')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active')
        labels = {'first_name': 'Nombre', 'last_name': 'Apellido',
                  'email': 'Correo', 'is_active': 'Usuario activo'}

    def __init__(self, *args, es_propio=False, **kwargs):
        super().__init__(*args, **kwargs)
        perfil, _ = Perfil.objects.get_or_create(usuario=self.instance)
        self.fields['rol'].initial = perfil.rol
        self.fields['telefono'].initial = perfil.telefono
        if es_propio:
            # Evita que el administrador se quite su propio rol o se desactive
            self.fields['rol'].disabled = True
            self.fields['is_active'].disabled = True

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            perfil, _ = Perfil.objects.get_or_create(usuario=user)
            perfil.rol = self.cleaned_data['rol']
            perfil.telefono = self.cleaned_data['telefono']
            perfil.save()
        return user
    
class PerfilForm(forms.ModelForm):
    telefono = forms.CharField(max_length=20, required=False, label='Telefono')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'first_name': 'Nombre', 'last_name': 'Apellido', 'email': 'Correo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        perfil, _ = Perfil.objects.get_or_create(usuario=self.instance)
        self.fields['telefono'].initial = perfil.telefono

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            perfil, _ = Perfil.objects.get_or_create(usuario=user)
            perfil.telefono = self.cleaned_data['telefono']
            perfil.save()
        return user