import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Cuestionario, DatoPersonal, SecDatoPersonal

    # Datos Personales
@login_required
def agregar_datoInv(request, cuestionario_id): #REVISAR
    if request.method != "POST":

        return JsonResponse(
            {'error':'Método inválido'},
            status=405
        )

    cuestionario = get_object_or_404(
        Cuestionario,
        id=cuestionario_id,
        usuario=request.user
    )

    sec2, _ = SecDatoPersonal.objects.get_or_create(
        cuestionario=cuestionario
    )

    dato = request.POST.get("dato")
    datosSensibles = (request.POST.get("datosSensibles") == "true")
    obtencionDatos = request.POST.get("obtencionDatos")
    medioObtencion = request.POST.get("medioObtencion")

    datosInv = DatoPersonal.objects.create(
        seccion=sec2,
        dato=dato,
        datosSensibles=datosSensibles,
        obtencionDatos=obtencionDatos,
        medioObtencion=medioObtencion
    )

    return JsonResponse({
        'success': True,

        'id': datosInv.id,

        'dato': datosInv.dato,
        'datosSensibles': datosInv.datosSensibles,
        'obtencionDatos': datosInv.get_obtencionDatos_display(),
        'medioObtencion': datosInv.get_medioObtencion_display(),
    })

@login_required
def datosPersonales_detalle(request, datoInv_id):
    datoInv = get_object_or_404(
        DatoPersonal,
        id=datoInv_id,
    )
    print(datoInv)

    # -------------------------------------------------------------
    # GET: Obtener
    # -------------------------------------------------------------
    if request.method == "GET":
        return JsonResponse({
            'success': True,

            'id': datoInv.id,

            'dato': datoInv.dato,
            'datosSensibles': datoInv.datosSensibles,
            'obtencionDatos': datoInv.obtencionDatos,
            'medioObtencion': datoInv.medioObtencion,
        })

    # -------------------------------------------------------------
    # PUT: Actualizar
    # -------------------------------------------------------------
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        # Actualizamos con fallback a los valores existentes por si la actualización es parcial
        print("contenido de data:")
        print(data)
        datoInv.dato = data.get("dato", datoInv.dato)
        datoInv.datosSensibles = (data.get("datosSensibles", datoInv.datosSensibles) == "true")
        datoInv.obtencionDatos = data.get("obtencionDatos", datoInv.obtencionDatos)
        datoInv.medioObtencion = data.get("medioObtencion", datoInv.medioObtencion)
        datoInv.save()

        return JsonResponse({
            'success': True,

            'id': datoInv.id,

            'dato': datoInv.dato,
            'datosSensibles': datoInv.datosSensibles,
            'obtencionDatos': datoInv.get_obtencionDatos_display(),
            'medioObtencion': datoInv.get_medioObtencion_display(),
        })

    # -------------------------------------------------------------
    # DELETE: Eliminar
    # -------------------------------------------------------------
    elif request.method == "DELETE":
        datoInv.delete()
        return JsonResponse({'success': True}, status=200)

    # -------------------------------------------------------------
    # Si intentan usar POST u otro metodo no permitido
    # -------------------------------------------------------------
    return JsonResponse({'error': 'Método no permitido'}, status=405)