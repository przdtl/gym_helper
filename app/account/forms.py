import uuid
from datetime import timedelta
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm, \
    PasswordResetForm, UsernameField, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from account.models import UserModel, EmailVerification
from django.contrib.auth import password_validation


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control', 'placeholder': "name@example.com"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control', 'placeholder': 'Password'}),
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'checked': ''}))

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'remember_me']


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': "Password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': 'Password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control', 'placeholder': "name"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "name@example.com"})
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user


class UpdatingUserForm(UserChangeForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-1'}),
        required=False,
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'image']


class ChangingPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, 'class': 'form-control'}
        ),
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )


class ResettingPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", 'class': 'form-control', 'placeholder': "name@example.com"}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = UserModel.objects.filter(email=email)
        if not user.exists() or not user.first().is_verified_email:
            raise ValidationError(
                'Данный email не привязан к какому-либо аккаунту'
            )


class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': "password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'class': 'form-control', 'placeholder': "password"}),
    )
