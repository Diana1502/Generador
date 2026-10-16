from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.db.models import Q

from .models import Sujeto

# Create your views here.
def vista_formulario(request, cuestionario_id):
    """
    Renderiza la página del formulario.
    Solo cargamos los elementos del Nivel 1 (los que no tienen padre)
    para el primer select de la interfaz.
    """
    secciones_raiz = Sujeto.objects.filter(padre__isnull=True)
    return render(request, 'padronso/formulario.html', {
        'secciones_raiz': secciones_raiz,
        'cuestionario_id': cuestionario_id
    })


def obtener_hijos(request, padre_id=None):
    """
    Endpoint tipo API que recibe un ID de padre y regresa sus hijos inmediatos en JSON.
    """
    if padre_id is None:
        elementos = Sujeto.objects.filter(padre__isnull=True)
    else:
        elementos = Sujeto.objects.filter(padre_id=padre_id)

    # Construimos una lista de diccionarios con los datos clave
    # 'es_final' usa la property 'es_hoja' que definimos en el modelo
    data = [
        {
            'id': e.id,
            'nombre': e.nombre,
            'es_final': e.es_hoja
        }
        for e in elementos
    ]

    return JsonResponse(data, safe=False)


def buscar_hijos(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 2:  # Solo buscamos si el usuario ha escrito al menos 2 caracteres
        return JsonResponse([], safe=False)

    # 1. Filtramos elementos que coincidan con el texto Y que no sean padres de nadie (hijos__isnull=True)
    resultados = Sujeto.objects.filter(
        Q(nombre__icontains=query),
        hijos__isnull=True  # <-- Esto garantiza que SOLO devuelva elementos finales/hijos
    )[:15]  # Limitamos a 15 resultados para mantener rápida la respuesta

    # 2. Formateamos la respuesta en JSON
    data = []
    for elem in resultados:
        # Opcional: Construir la ruta hacia arriba (ej: Padre > Hijo)
        ruta = []
        actual = elem
        while actual:
            ruta.append(actual.nombre)
            actual = actual.padre

        # Invertimos la lista para que quede "Raíz > Subnivel > Hijo"
        ruta_completa = " > ".join(reversed(ruta))

        data.append({
            'id': elem.id,
            'nombre': elem.nombre,
            'ruta_completa': ruta_completa
        })

    return JsonResponse(data, safe=False)