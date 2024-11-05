from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('actividades',views.listar_actividades,name='listar_actividades'),
    
    path('actividades/visitas/<int:actividad_id>/',views.listar_visitas_actividades,name='listar_visitas_actividades'),
    
    path('visitas/guias/<int:visita_id>/',views.listar_guias_visita,name='listar_guias_visita'), 
    
    path('visitas/guia/<int:guia_id>/<str:texto>/',views.listar_visitas_texto_guias,name='listar_visitas_texto_guias'),
    
    path('visitas/<int:anyo_desde>/<int:anyo_hasta>',views.listar_visitas_anyos,name='listar_visitas_anyos'), 
    
    path('cometario/ultimo/actividad/<int:actividad_id>/',views.ultimo_comentario_actividad,name='ultimo_comentario_actividad'),
    
    path('cometarios/visita/<int:visita_id>/<int:anyo>/<str:texto>/',views.listar_comentarios_filtro,name='listar_comentarios_filtro'),
    
    path('etiquetas/actividad/<int:actividad_id>/',views.listar_etiquetas_actividad,name='listar_etiquetas_actividad'),
    
]
