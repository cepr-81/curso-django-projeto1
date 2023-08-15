from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',
                  ]
        # exclude = ['first_name']

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'password': 'Password',
        }

        help_texts = {
            'email': 'Type a valid e-mail.'
        }

        error_messages = {
            'username': {
                'required': 'This field can not be empty.',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password'
            })
        }
