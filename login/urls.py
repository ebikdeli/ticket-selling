from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from . import forms_forget_passwords


app_name = 'login'

urlpatterns = [
     path('login-signup/', views.login_signup, name='login-signup'),
     path('login/', views.classic_login, name='classic-login'),
     path('logout/', views.logout_view, name='logout'),
     path('signup/', views.signup, name='signup'),
     path('password-change', views.password_change, name='password-change'),
     path('edit-profile', views.edit_profile, name='edit-profile'),
     path('edit-profile-image', views.edit_profile_image, name='edit-profile-image'),
]

urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='login/forget-password/password-reset.html',
                                              form_class=forms_forget_passwords.PasswordResetF,
                                              from_email='green_apple@gmail.com',
                                              # email_template_name='login/templates/forget_password/password_reset_email.html', OR below:
                                              email_template_name='login/forget-password/password-reset-email.html',
                                              success_url=reverse_lazy('login:password-reset-done')),
         name='password-reset'),

    path('password-reset-done/',
         auth_views.PasswordResetDoneView.as_view(template_name='login/forget-password/password-reset-done.html'),
         name='password-reset-done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='login/forget-password/password-reset-confirm.html',
                                                     form_class=forms_forget_passwords.SetPasswordF,
                                                     success_url=reverse_lazy('login:password-reset-complete'),
                                                     ),
         name='password-reset-confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='login/forget-password/password-reset-complete.html'),
         name='password-reset-complete')
]
