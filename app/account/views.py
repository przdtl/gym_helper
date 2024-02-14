from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView
from django.contrib import messages

from account.forms import LoginForm, RegisterForm, UpdatingUserForm, ChangingPasswordForm, ResettingPasswordForm, \
    SetNewPasswordForm
from account.models import UserModel, EmailVerification


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:index'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if user.is_verified_email:
            login(self.request, user)
            remember_me = form.cleaned_data['remember_me']
            if not remember_me:
                self.request.session.set_expiry(0)
                self.request.session.modified = True
        else:
            pass
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:index'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.info(self.request,
                      'Для подтверждения аккаунта перейдите по ссылке в письме, отправленном на адрес электронной почты, указанный при регистрации')
        form.save()
        return super().form_valid(form)


class UpdatingUserView(FormView):
    model = UserModel
    template_name = 'account/index.html'
    form_class = UpdatingUserForm
    success_url = reverse_lazy('account:index')

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.user.username
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def post(self, request, *args, **kwargs):
        form = UpdatingUserForm(data=request.POST, instance=request.user, files=request.FILES)
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ChangingPasswordView(PasswordChangeView):
    template_name = 'account/password_change.html'
    form_class = ChangingPasswordForm
    success_url = reverse_lazy('account:password_change')


class EmailVerificationView(TemplateView):
    template_name = 'account/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = UserModel.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(code=code, user=user)
        if email_verifications.exists() and not email_verifications.last().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


class EmailChangeView(TemplateView):
    template_name = 'account/email_change.html'


class ResettingPasswordView(PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = ResettingPasswordForm
    success_url = reverse_lazy('account:login')
    email_template_name = 'account/email/password_reset_email.txt'
    html_email_template_name = 'account/email/html_password_reset_email.html'
    subject_template_name = 'account/email/password_reset_subject.txt'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:index'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.info(self.request, 'На указанную почту было выслано письмо с ссылкой на страницу установки нового пароля')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/reset.html'
    form_class = SetNewPasswordForm
    success_url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:index'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Пароль был успешно установлен!')
        return super().form_valid(form)
