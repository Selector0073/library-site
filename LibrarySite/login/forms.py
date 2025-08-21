from .models import Login
from django.forms import ModelForm, TextInput

class LoginForm(ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'email', 'passw']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail'
            }),
            'passw': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }