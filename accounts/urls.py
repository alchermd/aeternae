from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password-reset.html',
            success_url=reverse_lazy("accounts:password-reset-done"),
            email_template_name='accounts/mail/password-reset.html',
        ),
        name="password-reset"
    ),
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password-reset-done.html'),
        name="password-reset-done"
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password-reset-confirm.html', success_url=reverse_lazy('accounts:password-reset-complete')),
        name="password-reset-confirm"
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password-reset-complete.html'),
        name="password-reset-complete"
    ),
]
