from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    aviso_privacidad = forms.BooleanField(
        required=True,
        label="Acepto el aviso de privacidad"
    )
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2','aviso_privacidad']