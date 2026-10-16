from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone

from .forms import RegistroForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('apps.cuestionarios:dashboard')

        messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'usuarios/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('apps.usuarios:login')


# @login_required
# def dashboard(request):
#     return render(request, 'cuestionarios/dashboard.html')



def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.fecha_aceptacion = timezone.now()
            user.save()
            print("Usuario creado:", user.username)

            messages.success(request, 'Usuario creado correctamente')
            return redirect('apps.usuarios:login')

    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def keep_alive(request):
    request.session.modified = True
    return JsonResponse({"status": "ok"})