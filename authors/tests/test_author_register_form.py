from unittest import TestCase

# from django.test import TestCase
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números '
         'e @/./+/-/_ apenas.'),
        ('email', 'Type a valid e-mail.'),
        ('password', ('Password must have at least one uppercase letter, '
                      'one lowercase letter and one number. The minimal '
                      'length should be at least 8 characters.'
                      )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confirm Password'),
    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(needed, current)
