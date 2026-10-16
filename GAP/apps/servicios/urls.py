from django.urls import path
from . import views

urlpatterns = [
    path('word/integral/<uuid:cuestionario_id>/', views.word_integral, name='Wordintegral'),
    path('word/simplificado/<uuid:cuestionario_id>/', views.word_simplificado, name='Wordsimplificado'),
]