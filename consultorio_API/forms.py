from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellido', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label='Teléfono', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model  = Usuario
        fields = [
            "username", "first_name", "last_name",
            "email", "telefono", "rol",
            "cedula_profesional", "institucion_cedula"
        ]
        widgets = {
            fname: forms.TextInput(attrs={"class": "form-control"})
            for fname in [
                "username", "first_name", "last_name",
                "email", "telefono", "cedula_profesional",
                "institucion_cedula"
            ]
        } | {
            "rol": forms.Select(attrs={"class": "form-select"})
        }

    # añade clases a los campos de contraseña
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


# ----------  EDITAR (incluye consultorio)  ----------
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model  = Usuario
        fields = [
            "username", "first_name", "last_name",
            "email", "telefono", "rol",
            "cedula_profesional", "institucion_cedula",
            "consultorio"
        ]
        widgets = {
            fname: forms.TextInput(attrs={"class": "form-control"})
            for fname in [
                "username", "first_name", "last_name",
                "email", "telefono", "cedula_profesional",
                "institucion_cedula"
            ]
        } | {
            "rol":         forms.Select(attrs={"class": "form-select"}),
            "consultorio": forms.Select(attrs={"class": "form-select"})
        }