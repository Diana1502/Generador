from django.contrib import admin
from .models import Cuestionario,Finalidad, SecResponsable, SecTratamiento, DatoPersonal, Fundamento, Destinatario, SecEjercicioARCO, SecUT, SecManifNegativa, SecCambiosAvP, SecInfoCompl, SecFundamento

# Register your models here.
admin.site.register(Cuestionario)


admin.site.register(SecResponsable)
admin.site.register(SecTratamiento)
admin.site.register(DatoPersonal)
admin.site.register(Fundamento)
admin.site.register(SecFundamento)
admin.site.register(Finalidad)
admin.site.register(SecEjercicioARCO)
admin.site.register(SecUT)
admin.site.register(Destinatario)
admin.site.register(SecManifNegativa)
admin.site.register(SecCambiosAvP)
admin.site.register(SecInfoCompl)

