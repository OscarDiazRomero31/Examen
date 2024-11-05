from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Guia(models.Model):
    nombre=models.CharField(max_length=50)
    email=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=20)
    fecha_registro=models.DateTimeField(default=timezone.now)
    
class Actividades(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion=models.TextField(max_length=2500) 
    duracion=models.FloatField()
    fecha_inicio=models.DateField(default=timezone.now)
    fecha_fin=models.DateField(default=timezone.now)
    
    colaboradores=models.ManyToManyField(Guia,related_name='colaboradores_visita')
    
    creador=models.ForeignKey(Guia,on_delete=models.CASCADE,related_name='creador_visita')
    
class Visita(models.Model):
    titulo=models.CharField(max_length=100) 
    descripcion=models.TextField()
    prioridad=models.IntegerField()
    
    ESTADOS=[('PE','Pendiente'),('PR','Progreso'),('Co','Completada')]
    estado=models.CharField(max_length=2,choices=ESTADOS)
    
    completada=models.BooleanField()
    fecha_creacion=models.DateField(default=timezone.now)
    hora_vencimiento=models.TimeField(default=timezone.now)
    
    
    creador=models.ForeignKey(Guia,on_delete=models.CASCADE,related_name="creador_visita")
    
    
    
    guias_asignados=models.ManyToManyField(Guia, through='asignacionVisita',
                                            related_name='guia_visita')
    
    
    actividad=models.ForeignKey(Actividades,on_delete=models.CASCADE,related_name="actividades_visita")
    
class AsignacionVisita(models.Model):
    usuario=models.ForeignKey(Guia,on_delete=models.CASCADE)
    tarea=models.ForeignKey(Visita,on_delete=models.CASCADE)
    observaciones=models.TextField(max_length=2500)
    fecha_asignacion=models.DateTimeField(default=timezone.now)

class Etiqueta(models.Model):
    nombre=models.CharField(max_length=30,unique=True)
    
    tarea=models.ManyToManyField(Visita,related_name="etiquetas_visitas")

class Comentario(models.Model):
    contenido=models.TextField(max_length=2500)
    fecha_comentario=models.DateTimeField(default=timezone.now)
    
    autor=models.ForeignKey(Guia,on_delete=models.CASCADE,related_name="comentarios_guias")
    
    tarea=models.ForeignKey(Visita,on_delete=models.CASCADE,related_name="comentarios_visitas")