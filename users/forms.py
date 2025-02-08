from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин или Email")
    
class RegistrationForm(UserCreationForm):
    patronymic = forms.CharField(label="Отчество", required=False)
    phone = forms.CharField(label="Телефон")
    
    class Meta:
        model = User
        fields = (
            'last_name', 
            'first_name', 
            'patronymic',
            'email',
            'phone',
            'password1', 
            'password2'
        )