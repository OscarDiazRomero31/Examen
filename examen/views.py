from django.shortcuts import render
from django.db.models import Q,Prefetch
from .models import Actividades,Visita,Guia,Comentario,Etiqueta

# Create your views here.
def index(request):
    return render(request, 'examen/index.html')

def listar_actividades(request):
    
    actividades = (Actividades.objects.select_related("creador")
                 .prefetch_related("colaboradores",Prefetch("actividades_visita"))
                ).all()
    return render(request, "actividades/lista.html", {"actividades":actividades})

def listar_visitas_actividades(request,actividades_id):
    actividad_mostrar = Actividades.objects.get(id=actividades_id)

    visitas = (Visita.objects.select_related("creador","actividad").
              prefetch_related("guias_asignados",Prefetch("etiquetas_visitas"),
                               Prefetch("comentarios_visita"),
                               Prefetch("comentarios_visita__autor")  
                               )
            )
    visitas = visitas.filter(actividades=actividades_id).order_by("-fecha_creacion").all()
    
    return render(request, "visitas/lista.html", {"visitas":visitas, "actividades":actividad_mostrar})

def listar_guias_visita(request,visita_id):
    visita = Visita.objects.get(id=visita_id)
    
   
    guias = (Guia.objects.prefetch_related(
                            Prefetch("creador_actividad"),
                            Prefetch("colaboradores_actividad"),
                            Prefetch("creador_visita"),
                            Prefetch("colaboradores_visita"),
                            Prefetch("comentarios_creador"),
                               )
                        .filter(asignacionvisita__visita=visita_id)
                        .order_by("asignacionvisita__fecha_asignacion")
    ).all()
    
    
    return render(request, "guia/lista_completa.html", {"guias":guias,"visita":visita})

def listar_visitas_texto_guias(request,guia_id,texto):
    guia = Guia.objects.get(id=guia_id)
    visitas = (Visita.objects.select_related("creador","actividades").
              prefetch_related("guias_asignados",Prefetch("etiquetas_visitas"),
                               Prefetch("comentarios_visita"),
                               Prefetch("comentarios_visita__autor")  
                                )
    ).filter(asignacionvisita__observaciones__contains=texto,asignacionvisita__guia=guia_id).all()
 
    return render(request, "visita/lista_filtro_guia.html", {"visitas":visitas, "guia": guia})

def listar_visitas_anyos(request,anyo_desde,anyo_hasta):
    visitas = (Visita.objects.select_related("creador","actividad").
              prefetch_related("guias_asignados",Prefetch("etiquetas_visitas"),
                               Prefetch("comentarios_visita"),
                               Prefetch("comentarios_visita__autor")  
                               )
    ).filter(fecha_creacion__year__gte=anyo_desde,fecha_creacion__year__lte=anyo_hasta,estado='Co')          
    return render(request, "visita/lista.html", {"visitas":visitas})

def ultimo_comentario_actividad(request,actividad_id):
    comentario = (Comentario.objects.select_related("autor","visita").
                   prefetch_related(Prefetch("visita__actividad"))
                  .filter(visita__actividad=actividad_id)
                  .order_by("-fecha_comentario")[0:1].get()                        
    )
    guia = comentario.autor
    
    return render(request, "guia/guia.html", {"guia":guia})

def listar_comentarios_filtro(request,visita_id,anyo,texto):
    visita = Visita.objects.get(id=visita_id)
    
    comentarios = (Comentario.objects.select_related("autor")
                  .filter(visita=visita_id)
                  .filter(fecha_comentario__year=anyo)
                  .filter(contenido__startswith=texto)
    ).all()
    
    return render(request, "comentario/lista.html", {"visita":visita,"comentarios":comentarios})

def listar_etiquetas_actividad(request,actividad_id):
    actividad = Actividades.objects.get(id=actividad_id)
    
    etiquetas = (Etiqueta.objects.prefetch_related("visita")
                 .filter(visita__actividad=actividad_id)
    ).distinct().all()
    
    return render(request, "etiqueta/lista.html", {"actividad":actividad,"etiquetas":etiquetas})

#Páginas de Error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
