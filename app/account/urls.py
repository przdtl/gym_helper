from django.urls import path, include
from account.views import LoginView, RegisterView, UpdatingUserView, ChangingPasswordView, \
    EmailVerificationView, EmailChangeView, ResettingPasswordView, MyPasswordResetConfirmView
from django.contrib.auth.decorators import login_required

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_change/', login_required(ChangingPasswordView.as_view()), name='password_change'),
    path('password_reset/', ResettingPasswordView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('change_email/', login_required(EmailChangeView.as_view()), name='change_email'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('', include('django.contrib.auth.urls'), name='django_auth'),
    path('', login_required(UpdatingUserView.as_view()), name='index'),
]
