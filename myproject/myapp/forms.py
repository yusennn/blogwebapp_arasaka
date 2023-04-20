from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .models import Post


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    error_messages = {
        'password_mismatch': _("Пароли не совпадают."),
        'password_too_similar': _("Пароль схож с адресом электронной почты."),
        'password_too_short': _("Пароль слишком легкий, необходимо как минимум 8 символов."),
        'password_too_common': _("Пароль слишком простой."),
        'password_entirely_numeric': _("Пароль не должен состоять только из цифр."),
    }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        email = self.cleaned_data.get("email")

        if email and password1 and email in password1:
            raise forms.ValidationError(
                self.error_messages['password_too_similar'],
                code='password_too_similar',
            )

        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_too_short'],
                code='password_too_short',
            )

        if password1.isdigit():
            raise forms.ValidationError(
                self.error_messages['password_entirely_numeric'],
                code='password_entirely_numeric',
            )

        return password1

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        error_messages = {
            'password_mismatch': _("Пароли не совпадают."),
        }


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserLogoutForm(forms.Form):
    pass


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']



