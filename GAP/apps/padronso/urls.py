from django.urls import path
from . import views

app_name = 'apps.padronso'

urlpatterns = [
    # path('formularioSO/', views.vista_formulario, name='vista_formulario'),
    path('formularioSO/<uuid:cuestionario_id>', views.vista_formulario, name='vista_formulario'),

    path('SO/hijos/', views.obtener_hijos, name='obtener_hijos_raiz'),
    path('SO/hijos/<int:padre_id>/', views.obtener_hijos, name='obtener_hijos'),

    path('SO/buscar-hijos/', views.buscar_hijos, name='buscar_hijos'),
]