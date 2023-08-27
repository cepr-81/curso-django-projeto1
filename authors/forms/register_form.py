from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    username = forms.CharField(
        error_messages={
            'required': 'This field can not be empty.',
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'Username must have 150 characters or less.'},
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those e @.+-_. '
            'The length should be between 4 and 150 characters.'),
        min_length=4,
        max_length=150,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name.'},
        label='First Name',
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name.'},
        label='Last Name',
    )

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required.'},
        label='E-mail',
        help_text='Type a valid e-mail.',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password can not be empty.'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The minimal length '
            'should be at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirm Password',
        error_messages={
            'required': 'Please, repeat your password.'
        },
    )

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',
                  ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('E-mail already exists', code='invalid',)

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Passwords must be equal.',
                'password2': 'Passwords must be equal.',
            })
