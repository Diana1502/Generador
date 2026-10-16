from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse

from ..models import Municipio

@login_required
def cargar_municipios(request):
    estado_id = request.GET.get("estado")
    municipios = Municipio.objects.filter(estado_id=estado_id).values("id", "nombre")
    return JsonResponse(list(municipios), safe=False)