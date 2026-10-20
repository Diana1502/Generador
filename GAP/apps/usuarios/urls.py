from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'apps.usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('ingresoCorreo/',
         auth_views.PasswordResetView.as_view(
             template_name='usuarios/ingresoCorreo.html',
             email_template_name='usuarios/password_reset_email.html',
             success_url=reverse_lazy('apps.usuarios:password_reset_done')
         ),
         name='password_reset'),

    path('mensaje/enviado/',
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/mensaje.html'),
         name='password_reset_done'),

    path('ingresoContrasenia/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/ingresoContrasenia.html',
             success_url=reverse_lazy('apps.usuarios:password_reset_complete')
         ),
         name='password_reset_confirm'),

    path('mensajeFinal/completo/',
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/mensajeFinal.html'),
         name='password_reset_complete'),
]