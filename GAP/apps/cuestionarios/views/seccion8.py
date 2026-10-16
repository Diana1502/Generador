import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Cuestionario, Destinatario, SecTransferencias

#   Transferencias
@login_required
def agregar_transferenciaInv(request, cuestionario_id):
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

    sec7, _ = SecTransferencias.objects.get_or_create(
        cuestionario=cuestionario
    )

    destinatario = request.POST.get("destinatario")
    consentimiento = (request.POST.get("consentimiento") == "true")
    tipoConsentimiento = request.POST.get("tipoConsentimiento")

    finalidades_ids = request.POST.getlist("finalidades[]")
    transferenciaInv = Destinatario.objects.create(
        seccion=sec7,
        destinatario=destinatario,
        consentimiento=consentimiento,
        tipoConsentimiento=tipoConsentimiento
    )

    transferenciaInv.finalidad.set(finalidades_ids)

    return JsonResponse({
        'success': True,

        'id': transferenciaInv.id,

        'destinatario': transferenciaInv.destinatario,
        'consentimiento': transferenciaInv.consentimiento,
        'tipoConsentimiento': transferenciaInv.get_tipoConsentimiento_display(),
        'finalidades': list(
            transferenciaInv.finalidad.values_list("finalidad")
        )
    })

@login_required
def transferenciaInv_detalle(request, transferenciaInv_id):
    transferenciaInv = get_object_or_404(
        Destinatario,
        id=transferenciaInv_id,
        seccion__cuestionario__usuario=request.user
    )
    print(transferenciaInv)

    # -------------------------------------------------------------
    # GET: Obtener
    # -------------------------------------------------------------
    if request.method == "GET":
        return JsonResponse({
            'success': True,

            'id': transferenciaInv.id,

            'destinatario': transferenciaInv.destinatario,
            'consentimiento': transferenciaInv.consentimiento,
            'tipoConsentimiento': transferenciaInv.tipoConsentimiento,
            'finalidades': list(
                transferenciaInv.finalidad.values_list("finalidad")  # revisar   OCUPAMOS NUMEROS
            )
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
        transferenciaInv.destinatario = data.get("destinatario", transferenciaInv.destinatario)
        transferenciaInv.consentimiento = (data.get("consentimiento", transferenciaInv.consentimiento) == "true")
        transferenciaInv.tipoConsentimiento = data.get("tipoConsentimiento", transferenciaInv.tipoConsentimiento)
        transferenciaInv.save()

        transferenciaInv.finalidad.set(data.get("finalidades", []))

        return JsonResponse({
            'success': True,

            'id': transferenciaInv.id,

            'destinatario': transferenciaInv.destinatario,
            'consentimiento': transferenciaInv.consentimiento,
            'tipoConsentimiento': transferenciaInv.get_tipoConsentimiento_display(),
            'finalidades': list(
                transferenciaInv.finalidad.values_list("finalidad")
            )
        })

    # -------------------------------------------------------------
    # DELETE: Eliminar
    # -------------------------------------------------------------
    elif request.method == "DELETE":
        transferenciaInv.delete()
        return JsonResponse({'success': True}, status=200)

    # -------------------------------------------------------------
    # Si intentan usar POST u otro metodo no permitido
    # -------------------------------------------------------------
    return JsonResponse({'error': 'Método no permitido'}, status=405)