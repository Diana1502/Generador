"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Vista para manejar la raíz "/"
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('apps.cuestionarios:dashboard')  # Redirige al dashboard en App1
    return redirect('apps.usuarios:login')         # Redirige al login en App2

urlpatterns = [
    path('', home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('', include('apps.cuestionarios.urls')),
    path('', include('apps.servicios.urls')),
    path('', include('apps.padronso.urls')),
]
