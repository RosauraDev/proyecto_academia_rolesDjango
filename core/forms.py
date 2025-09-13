from django import forms
from django.contrib.auth.models import User #modelo de django
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    email= forms.EmailField(label='Email')
    first_name=forms.CharField(label='Name: ')
    last_name= forms.CharField(label='Last name:')

    class Meta:
        model = User # modelo de django
        fields=['username', 'email', 'first_name','last_name','password1', 'password2']

    #validar si el correo ya existe
    def clean_email(self):
        email_field = self.cleaned_data['email'] # trae la información del email - del formulario

        if User.objects.filter(email=email_field).exists(): #valida si ya existe el correo
            raise forms.ValidationError('Este correo electronico ya esta registrado')
        return email_field


