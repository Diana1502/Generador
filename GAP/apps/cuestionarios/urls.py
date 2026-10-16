from django.urls import path
from . import views
from ..usuarios.urls import app_name

app_name = 'apps.cuestionarios'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'), #Pagina principal
    path('aviso-de-privacidad/', views.nuevo, name='nuevoAvP'),
    path('aviso-de-privacidad/<uuid:cuestionario_id>/iniciar/', views.iniciar, name='iniciar'),
    path('aviso-de-privacidad/<uuid:cuestionario_id>/continuar/', views.continuar, name='continuar'),
    path('aviso-de-privacidad/<uuid:cuestionario_id>/seccion/<int:numero>/', views.seccion, name='seccion'),
    path('aviso-de-privacidad/<uuid:cuestionario_id>/eliminar/', views.eliminar, name='eliminar'),
    # path('aviso-de-privacidad/<uuid:cuestionario_id>/', views.cuestionario_detalle, name='urlcuestionario'),

    # Municipios
    # path("ver-municipios/", views.municipios_view, name="municipios_view"),
    path("cargar-municipios/", views.cargar_municipios, name="cargar_municipios"),

    # Datos Personales
    path("aviso-de-privacidad/<uuid:cuestionario_id>/datos/", views.agregar_datoInv, name="agregar_datoInv"),
    path("datos/<int:datoInv_id>/", views.datosPersonales_detalle, name="urldatosInv"),

    # Fundamento Legal
    path("aviso-de-privacidad/<uuid:cuestionario_id>/fundamentoLegal/", views.agregar_fundamentoInv, name="agregar_fundamentoInv"),
    path("fundamentoLegal/<int:fundamentoInv_id>/", views.fundamentoInv_detalle, name="urlfundamentoInv"),

    # Finalidades
    path("aviso-de-privacidad/<uuid:cuestionario_id>/finalidad/", views.agregar_finalidadInv, name="agregar_finalidadInv"),
    path("finalidad/<int:finalidadInv_id>/", views.finalidadInv_detalle, name="urlfinalidadInv"),

    # Transferencias
    path("aviso-de-privacidad/<uuid:cuestionario_id>/transferencia/", views.agregar_transferenciaInv, name="agregar_transferenciaInv"),
    path("transferencia/<int:transferenciaInv_id>/", views.transferenciaInv_detalle, name="urltransferenciaInv"),

]

