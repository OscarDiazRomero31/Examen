
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('examen.urls')),
]

from django.conf.urls import handler400,handler404,handler403,handler500
handler404 = "examen.views.mi_error_400"
handler503 = "examen.views.mi_error_403"
handler503 = "examen.views.mi_error_404"
handler500 = "examen.views.mi_error_500"