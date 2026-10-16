# from django.contrib import admin
# from .models import Usuario
#
# # Register your models here.
# admin.site.register(Usuario)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Opcional: personaliza qué columnas se ven en la lista
    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)
