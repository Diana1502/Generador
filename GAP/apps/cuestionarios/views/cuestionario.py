import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Cuestionario, SecResponsable, Municipio, Finalidad, SecInfoCompl, SecTransferencias, Destinatario

from ..forms import SecManifNegaForm, SecTratamientoForm, SecFundamentoForm, SecFinalidadesForm, SecTransferenciasForm, SecDatoPersonalForm
from ..forms import (CuestionarioForm, SecResponsableForm, SecInfoComplForm, SecEjercicioARCOForm, SecUTForm, SecCambiosAvPForm, SecPortabilidadForm)
from ..models import DatoPersonal, SecEjercicioARCO, SecUT, SecCambiosAvP,SecManifNegativa, SecTratamiento, Fundamento, SecFundamento, SecFinalidad, SecDatoPersonal, SecPortabilidad


# Crear AvP
@login_required
def nuevo(request):
    print(request)
    if request.method == 'POST':
        form = CuestionarioForm(request.POST)
        if form.is_valid():
            cuestionario = form.save(commit=False)
            cuestionario.usuario = request.user
            cuestionario.save()  # Ahora sí se guarda en la base de datos con el nickname y el usuario

            return redirect('apps.padronso:vista_formulario', cuestionario.id)
    else:
        form = CuestionarioForm()

        return render(request, 'apps.cuestionarios:dashboard', {'form': form})

# Avp
@login_required
def cuestionario_detalle(request, cuestionario_id):
    c = get_object_or_404(Cuestionario, id=cuestionario_id, usuario=request.user)
    print(c)

    # -------------------------------------------------------------
    # GET: Obtener
    # -------------------------------------------------------------
    if request.method == "GET":
        return redirect('apps.cuestionarios:seccion', c.id, c.seccion_actual)

    # -------------------------------------------------------------
    # PUT: Actualizar
    # -------------------------------------------------------------
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return redirect('apps.cuestionarios:dashboard')

        # Actualizamos con fallback a los valores existentes por si la actualización es parcial
        c.sujetoObligado = data.get("nombrePadron", c.sujetoObligado)
        c.save(update_fields=["sujetoObligado"])

        return redirect('apps.cuestionarios:seccion', c.id, c.seccion_actual)

    # -------------------------------------------------------------
    # DELETE: Eliminar
    # -------------------------------------------------------------
    elif request.method == "DELETE":
        c.delete()
        return redirect('apps.cuestionarios:dashboard')

    # -------------------------------------------------------------
    # Si intentan usar POST u otro metodo no permitido
    # -------------------------------------------------------------
    return JsonResponse({'error': 'Método no permitido'}, status=405)




# Inicializar AvP con Sujeto Obligado
@login_required
def iniciar(request, cuestionario_id):
    c = get_object_or_404(Cuestionario, id=cuestionario_id, usuario=request.user)

    nombrePadron = request.GET.get("nombrePadron")

    if not nombrePadron:
        return redirect('apps.cuestionarios:dashboard')

    if not c.sujetoObligado:
        c.sujetoObligado = nombrePadron
        c.save(update_fields=["sujetoObligado"])

    return redirect('apps.cuestionarios:seccion', c.id, c.seccion_actual)



# Continuar AvP *
@login_required
def continuar(request, cuestionario_id):
    c = get_object_or_404(Cuestionario, id=cuestionario_id, usuario=request.user)

    return redirect('apps.cuestionarios:seccion', c.id, c.seccion_actual)

#
# Eliminar AvP *
@login_required
def eliminar(request, cuestionario_id):
    c = get_object_or_404(Cuestionario, id=cuestionario_id, usuario=request.user)
    c.delete()

    return redirect('apps.cuestionarios:dashboard')

# Secciones
SECCIONES = {
    1: {
        'form': SecResponsableForm,
        'model': SecResponsable,
        'template': 'cuestionarios/seccion1.html'
    },
    2: {
        'form': SecTratamientoForm,
        'model': SecTratamiento,
        'template': 'cuestionarios/seccion2.html'
    },
    3: {
        'form': SecFundamentoForm,
        'model': SecFundamento,
        'template': 'cuestionarios/seccion3.html'
    },
    4: {
        'form': SecFundamentoForm,
        'model': SecFundamento,
        'template': 'cuestionarios/seccion4.html'
    },
    5: {
        'form': SecFinalidadesForm,
        'model': SecFinalidad,
        'template': 'cuestionarios/seccion5.html'
    },
    6: {
        'form': SecEjercicioARCOForm,
        'model': SecEjercicioARCO,
        'template': 'cuestionarios/seccion6.html'
    },
    7: {
        'form': SecUTForm,
        'model': SecUT,
        'template': 'cuestionarios/seccion7.html'
    },
    8: {
         'form': SecTransferenciasForm,
         'model': SecTransferencias,
         'template': 'cuestionarios/seccion8.html'
    },
    9: {
        'form': SecManifNegaForm,
        'model': SecManifNegativa,
        'template': 'cuestionarios/seccion9.html'
    },
    10: {
        'form': SecCambiosAvPForm,
        'model': SecCambiosAvP,
        'template': 'cuestionarios/seccion10.html'
    },
    11: {
        'form': SecPortabilidadForm,
        'model': SecPortabilidad,
        'template': 'cuestionarios/seccion11.html'
    },
    12: {
        'form': SecInfoComplForm,
        'model': SecInfoCompl,
        'template': 'cuestionarios/seccion12.html'
    },
}

@login_required
def seccion(request, cuestionario_id, numero):
    print("METHOD:", request.method)

    # validar acceso al dueño
    cuestionario = get_object_or_404(
        Cuestionario, id=cuestionario_id, usuario=request.user
    )
    if numero >= 12: # Limite de secciones
        numero = 12


    # secciones del cuestionario
    if numero > cuestionario.seccion_actual:
        return redirect(
            'apps.cuestionarios:seccion',
            cuestionario_id=cuestionario.id,
            numero=cuestionario.seccion_actual
        )

    config = SECCIONES.get(numero)
    if not config:
        raise Http404()

    # ----------------------------
    # CASO FORM NORMAL
    # ----------------------------
    instance = (
        config["model"]
        .objects
        .filter(cuestionario=cuestionario)
        .first()
    )

    form = config['form'](
        request.POST or None,
        instance=instance
    )

    if request.method == 'POST':
        print("POST DATA:", request.POST)
        print("CUESTIONARIO:", instance)
        print("ERRORES:", form.errors)

    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.cuestionario = cuestionario
        obj.save()

        # avanzar sección
        if numero == cuestionario.seccion_actual:
            if numero <= 11:
                cuestionario.seccion_actual += 1

            if numero == 12:
                cuestionario.completado = True

            cuestionario.save()

        return redirect(
            'apps.cuestionarios:seccion',
            cuestionario_id=cuestionario.id,
            numero=cuestionario.seccion_actual
        )

    context = {
        'form': form,
        'cuestionario': cuestionario,
        'numero': numero
    }

    # SOLO sección 1
    if numero == 1:
        context['sujetoObligado'] = cuestionario.sujetoObligado

    # SOLO sección 3
    if numero == 3:
        sec3 = SecDatoPersonal.objects.filter(cuestionario=cuestionario).first()

        context['fundamentos'] = (
            DatoPersonal.objects.filter(
                seccion=sec3
            ) if sec3 else []
        )

    # SOLO sección 3
    if numero == 4:
        sec3 = SecFundamento.objects.filter(cuestionario=cuestionario).first()

        context['fundamentos'] = (
            Fundamento.objects.filter(
                seccion=sec3
            ) if sec3 else []
        )

    # SOLO sección 4
    if numero == 5:
        sec4 = SecFinalidad.objects.filter(cuestionario=cuestionario).first()

        context['finalidades'] = (
            Finalidad.objects.filter(
                seccion=sec4
            ) if sec4 else []
        )

    # SOLO seccion   - direccion
    if numero == 6:
        sec1 = SecResponsable.objects.filter(cuestionario=cuestionario).first()
        context['directorio'] = sec1.direccion_texto()
        context['responsable'] = sec1

    if numero == 7:
        sec1 = SecResponsable.objects.filter(cuestionario=cuestionario).first()
        context['directorio'] = sec1.direccion_texto()
        context['responsable'] = sec1

        sec6 = SecEjercicioARCO.objects.filter(cuestionario=cuestionario).first()
        if sec6.direccion_texto() != sec1.direccion_texto():
            context['directorio1'] = sec6.direccion_texto()
            context['responsable1'] = sec6


    # SOLO sección 7
    if numero == 8:
        sec7 = SecTransferencias.objects.filter(cuestionario=cuestionario).first()

        context['finalidades'] = Finalidad.objects.filter(seccion__cuestionario=cuestionario)

        context['destinatarios'] = (
            Destinatario.objects.filter(
                seccion=sec7
            ) if sec7 else []
        )

    return render(
        request,
        config['template'],
        context
    )

@login_required
def dashboard(request):
    lista_cuestionarios = Cuestionario.objects.filter(usuario=request.user).order_by('-creado')

    # Creamos el formulario vacío en memoria (operación ultra ligera)
    form_nuevo = CuestionarioForm()

    # Paginado de AvPs
    paginator = Paginator(lista_cuestionarios, 5)  # Muestra 5 por página
    page_number = request.GET.get('page')
    cuestionarios = paginator.get_page(page_number)

    return render(request, 'cuestionarios/dashboard.html', {
        'cuestionarios': cuestionarios,
        'form': form_nuevo
    })
