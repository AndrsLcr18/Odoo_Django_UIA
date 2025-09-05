from django.urls import path
from . import views

urlpatterns = [
#    path('', views.get_odoo_students, name='lista_estudiantes_root'),  # /solicitudes/ esto fue prueba
#    path('estudiantes/', views.get_odoo_students, name='estudiantes'),  # /solicitudes/estudiantes/ esto fue prueba
    path('buscar_estudiante/', views.buscar_estudiante, name='buscar_estudiante'),  # /solicitudes/buscar_estudiante/
    path('nueva_solicitud/', views.nueva_solicitud, name='nueva_solicitud'),    # /solicitudes/nueva_solicitud/
]
