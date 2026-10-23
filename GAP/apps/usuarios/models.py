from django.contrib.auth import user_logged_in
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


class Usuario(AbstractUser):
    aviso_privacidad = models.BooleanField(default=False)
    fechaAceptaAvP = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username


# Función para cerrar sesiones simultaneas
@receiver(user_logged_in)
def cerrar_sesiones_simultaneas(sender, user, request, **kwargs):

    #Aseguramos que la sesión actual ya tenga una clave generada
    if not request.session.session_key:
        request.session.create()

    clave_sesion_actual = request.session.session_key

    #Obtenemos todas las sesiones activas en la base de datos
    sesiones_activas = Session.objects.filter(expire_date__gte=timezone.now())

    #Revisamos una por una a quién le pertenecen
    for sesion in sesiones_activas:
        datos_sesion = sesion.get_decoded()

        #Si el ID del usuario de la sesión coincide con el usuario que está entrando...
        if str(datos_sesion.get('_auth_user_id')) == str(user.id):

            # ...y la sesión no es la que acaba de abrir, la borramos.
            if sesion.session_key != clave_sesion_actual:
                sesion.delete()


