import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Cuestionario, Finalidad, SecFinalidad

# Finalidades
@login_required
def agregar_finalidadInv(request, cuestionario_id):
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

    sec4, _ = SecFinalidad.objects.get_or_create(
        cuestionario=cuestionario
    )

    finalidad = request.POST.get("finalidad")
    necesaria = (request.POST.get("necesaria") == "true")
    reqConsentimiento = (request.POST.get("reqConsentimiento") == "true")
    tipoConsentimiento = request.POST.get("tipoConsentimiento")
    finPrincipal = (request.POST.get("finPrincipal") == "true")

    finalidadInv = Finalidad.objects.create(
        seccion=sec4,
        finalidad=finalidad,
        necesaria=necesaria,
        reqConsentimiento=reqConsentimiento,
        tipoConsentimiento=tipoConsentimiento,
        finPrincipal=finPrincipal
    )

    return JsonResponse({
        'success': True,

        'id': finalidadInv.id,

        'finalidad': finalidadInv.finalidad,
        'necesaria': finalidadInv.necesaria,
        'reqConsentimiento': finalidadInv.reqConsentimiento,
        'tipoConsentimiento': finalidadInv.get_tipoConsentimiento_display(),
        'finPrincipal': finalidadInv.finPrincipal,
    })

@login_required
def finalidadInv_detalle(request, finalidadInv_id):
    finalidadInv = get_object_or_404(
        Finalidad,
        id=finalidadInv_id,
        seccion__cuestionario__usuario=request.user
    )
    print(finalidadInv)

    # -------------------------------------------------------------
    # GET: Obtener
    # -------------------------------------------------------------
    if request.method == "GET":
        return JsonResponse({
            'success': True,

            'id': finalidadInv.id,

            'finalidad': finalidadInv.finalidad,
            'necesaria': finalidadInv.necesaria,
            'reqConsentimiento': finalidadInv.reqConsentimiento,
            'tipoConsentimiento': finalidadInv.tipoConsentimiento,
            'finPrincipal': finalidadInv.finPrincipal,
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
        finalidadInv.finalidad = data.get("finalidad", finalidadInv.finalidad)
        finalidadInv.necesaria = (data.get("necesaria", finalidadInv.necesaria) == "true")
        finalidadInv.reqConsentimiento = (data.get("reqConsentimiento", finalidadInv.reqConsentimiento) == "true")
        finalidadInv.tipoConsentimiento = data.get("tipoConsentimiento", finalidadInv.tipoConsentimiento)
        finalidadInv.finPrincipal = (data.get("finPrincipal", finalidadInv.finPrincipal) == "true")

        finalidadInv.save()

        return JsonResponse({
            'success': True,

            'id': finalidadInv.id,

            'finalidad': finalidadInv.finalidad,
            'necesaria': finalidadInv.necesaria,
            'reqConsentimiento': finalidadInv.reqConsentimiento,
            'tipoConsentimiento': finalidadInv.get_tipoConsentimiento_display(),
            'finPrincipal': finalidadInv.finPrincipal,
        })

    # -------------------------------------------------------------
    # DELETE: Eliminar
    # -------------------------------------------------------------
    elif request.method == "DELETE":
        finalidadInv.delete()
        return JsonResponse({'success': True}, status=200)

    # -------------------------------------------------------------
    # Si intentan usar POST u otro metodo no permitido
    # -------------------------------------------------------------
    return JsonResponse({'error': 'Método no permitido'}, status=405)

