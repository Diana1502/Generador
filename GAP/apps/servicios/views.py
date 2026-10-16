from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, JsonResponse

from datetime import datetime

from apps.cuestionarios.models import Cuestionario, SecResponsable, SecTratamiento, SecEjercicioARCO, SecUT, \
    SecManifNegativa, SecFundamento, Fundamento, SecCambiosAvP, SecFinalidad, Finalidad, SecDatoPersonal, DatoPersonal, \
    SecPortabilidad, SecTransferencias, Destinatario, SecInfoCompl
from apps.servicios.models import GeneradorAvisoPrivacidad

# -------------- Validar la completitud del documento, en casos contrario mandar alerta

### GLOBALES
MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}

# Word Integral AvP
@login_required
def word_integral(request, cuestionario_id):
    c = get_object_or_404(Cuestionario, id=cuestionario_id, usuario=request.user)
    sec1= get_object_or_404(SecResponsable, cuestionario = c)
    sec2 = get_object_or_404(SecTratamiento, cuestionario = c)
    sec21_datosp = get_object_or_404(SecDatoPersonal, cuestionario = c)
    datosp = DatoPersonal.objects.filter(seccion=sec21_datosp) if sec21_datosp else []
    sec3 = SecFundamento.objects.filter(cuestionario = c).first()
    fundamentos =Fundamento.objects.filter(seccion=sec3) if sec3 else []
    sec4 = SecFinalidad.objects.filter(cuestionario = c).first()
    finalidad = Finalidad.objects.filter(seccion=sec4) if sec4 else []
    sec5 = get_object_or_404(SecEjercicioARCO, cuestionario = c)
    sec8 = get_object_or_404(SecManifNegativa, cuestionario = c)
    sec9 = get_object_or_404(SecCambiosAvP, cuestionario = c)
    sec6 = get_object_or_404(SecUT, cuestionario = c)
    sec7 = get_object_or_404(SecTransferencias, cuestionario = c)
    destinos = Destinatario.objects.filter(seccion=sec7) if sec7 else []
    sec11 = get_object_or_404(SecPortabilidad, cuestionario = c)
    sec12 = get_object_or_404(SecInfoCompl, cuestionario = c)

    generador = GeneradorAvisoPrivacidad()

    hoy = datetime.now()
    # Esta es la línea que genera la fecha:
    fecha_hoy = f"{hoy.day} de {MESES[hoy.month]} de {hoy.year}"
    print(fecha_hoy)

    nombrearchivo = "aviso_privacidad_Integral_" + c.nickname + ".docx"
    nombrearchivo = generador.obtener_nombre_unico(nombrearchivo)

    generador.completar_datos(c, fecha_hoy,sec1,sec2)
    generador.crearDocto(nombrearchivo)

    generador.escribir_titulo("INTEGRAL")
    generador.escribir_seccion1(sec1)
    generador.escribir_seccion2(datosp)
    generador.escribir_seccion3(fundamentos)
    generador.escribir_seccion4(finalidad)
    generador.escribir_seccion5_6(sec5,sec6)
    generador.escribir_seccion7(destinos)
    generador.escribir_seccion8(sec8)
    generador.escribir_seccion9(sec9)
    generador.escribir_portabilidad(sec11)
    generador.escribir_infoAdicional(sec12.observaciones)
    generador.escribir_fecha()

    # return FileResponse(
    #     open(nombrearchivo, "rb"),
    #     as_attachment= True,
    #     filename= nombrearchivo
    # )
    return redirect('apps.cuestionarios:dashboard') # Agregar imagen de creando o descargando


# Word Integral AvP
@login_required
def word_simplificado(request, cuestionario_id):
    c = get_object_or_404(Cuestionario, id=cuestionario_id, usuario=request.user)
    sec1= get_object_or_404(SecResponsable, cuestionario = c)
    sec2 = get_object_or_404(SecTratamiento, cuestionario = c)
    sec4 = SecFinalidad.objects.filter(cuestionario = c).first()
    finalidad = Finalidad.objects.filter(seccion=sec4) if sec4 else []
    sec5 = get_object_or_404(SecEjercicioARCO, cuestionario = c)
    sec7 = get_object_or_404(SecTransferencias, cuestionario=c)
    destinos = Destinatario.objects.filter(seccion=sec7) if sec7 else []
    sec8 = get_object_or_404(SecManifNegativa, cuestionario = c)
    sec9 = get_object_or_404(SecCambiosAvP, cuestionario = c)
    sec6 = get_object_or_404(SecUT, cuestionario = c)

    generador = GeneradorAvisoPrivacidad()

    hoy = datetime.now()
    # Esta es la línea que genera la fecha:
    fecha_hoy = f"{hoy.day} de {MESES[hoy.month]} de {hoy.year}"
    print(fecha_hoy)

    nombrearchivo = "aviso_privacidad_Simplificado_" + c.nickname + ".docx"
    nombrearchivo = generador.obtener_nombre_unico(nombrearchivo)

    generador.completar_datos(c, fecha_hoy,sec1,sec2)
    generador.crearDocto(nombrearchivo)

    generador.escribir_titulo("SIMPLIFICADO")
    generador.escribir_seccion1(sec1)
    generador.escribir_seccion4(finalidad, "II")
    generador.escribir_seccion7(destinos,  "III")
    generador.escribir_seccion8(sec8, "IV")
    generador.escribir_conocerAvP(sec9)
    generador.escribir_fecha()

    return redirect('apps.cuestionarios:dashboard') # Agregar imagen de creando o descargando
