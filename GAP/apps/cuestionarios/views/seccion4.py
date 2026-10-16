import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Cuestionario, Fundamento, SecFundamento

    # Fundamento Legal
@login_required
def agregar_fundamentoInv(request, cuestionario_id):
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

    sec3, _ = SecFundamento.objects.get_or_create(
        cuestionario=cuestionario
    )

    ley = request.POST.get("ley")
    especificacion = request.POST.get("especificacion")

    fundamentoInv = Fundamento.objects.create(
        seccion=sec3,
        ley=ley,
        especificacion=especificacion
    )

    return JsonResponse({
        'success': True,

        'id': fundamentoInv.id,

        'ley': fundamentoInv.ley,
        'especificacion': fundamentoInv.especificacion,
    })

@login_required
def fundamentoInv_detalle(request, fundamentoInv_id):
    fundamentoInv = get_object_or_404(
        Fundamento,
        id=fundamentoInv_id,
        seccion__cuestionario__usuario=request.user
    )
    print(fundamentoInv)

    # -------------------------------------------------------------
    # GET: Obtener
    # -------------------------------------------------------------
    if request.method == "GET":
        return JsonResponse({
            'success': True,

            'id': fundamentoInv.id,

            'ley': fundamentoInv.ley,
            'especificacion': fundamentoInv.especificacion,
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
        fundamentoInv.ley = data.get("ley", fundamentoInv.ley)
        fundamentoInv.especificacion = data.get("especificacion", fundamentoInv.especificacion)
        fundamentoInv.save()

        return JsonResponse({
            'success': True,

            'id': fundamentoInv.id,

            'ley': fundamentoInv.ley,
            'especificacion': fundamentoInv.especificacion,
        })

    # -------------------------------------------------------------
    # DELETE: Eliminar
    # -------------------------------------------------------------
    elif request.method == "DELETE":
        fundamentoInv.delete()
        return JsonResponse({'success': True}, status=200)

    # -------------------------------------------------------------
    # Si intentan usar POST u otro metodo no permitido
    # -------------------------------------------------------------
    return JsonResponse({'error': 'Método no permitido'}, status=405)