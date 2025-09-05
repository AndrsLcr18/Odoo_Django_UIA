# -*- coding: utf-8 -*-
# Vistas para manejar solicitudes de estudiantes 
from django.shortcuts import render, redirect
from .odoo_rpc import OdooRPC
import base64
from datetime import datetime, date


odoo = OdooRPC()

# ------------------------------
# Buscar estudiante
# ------------------------------
def buscar_estudiante(request):
    context = {}
    if request.method == "POST":
        identificacion = request.POST.get("identificacion")
        try:
            # Traer información del estudiante
            estudiantes = odoo.call(
                "tcu.estudiante",
                "search_read",
                args=[[["identificacion", "=", identificacion]]],
                kwargs={"fields": [
                    "name",
                    "identificacion",
                    "carnet",
                    "correo",
                    "telefono",
                    "periodo_id",
                    "lugar_tcu",
                    "encargado_estudiante",
                    "fecha_solicitud",
                    "estado_solicitud",
                    "observaciones",
                    "motivo_estado",
                    "carta_aceptacion",
                    "carta_aceptacion_filename"
                ]}
            )

            # DEBUG: imprime lo que devuelve Odoo en la consola no borrar
            print("ESTUDIANTES:", estudiantes)

            context["info"] = estudiantes

        except Exception as e:
            context["info"] = []
            context["error"] = str(e)

    return render(request, "solicitudes/buscar_estudiante.html", context)

# ------------------------------
# Crear nueva solicitud
# ------------------------------
def nueva_solicitud(request):
    periodos = odoo.call("tcu.periodo", "search_read", args=[[], ["name", "anio", "activo"]])
    fecha_hoy = date.today().isoformat()

    if request.method == "POST":
        # campos del formulario
        data = {
            "name": request.POST.get("name") or "",  
            "identificacion": request.POST.get("identificacion") or "",
            "carnet": request.POST.get("carnet") or "",
            "correo": request.POST.get("correo") or "",
            "telefono": request.POST.get("telefono") or "",
            "periodo_id": int(request.POST.get("periodo_id") or 0),
            "lugar_tcu": request.POST.get("lugar_tcu") or "",
            "encargado_estudiante": request.POST.get("encargado_estudiante") or "",
            "fecha_solicitud": request.POST.get("fecha_solicitud") or fecha_hoy,
            "observaciones": request.POST.get("observaciones") or "",
            "motivo_estado": request.POST.get("motivo_estado") or "",
            "estado_solicitud": "en_revision",
        }

        # Archivo adjunto
        archivo_file = request.FILES.get("archivo")
        if archivo_file:
            data["carta_aceptacion"] = base64.b64encode(archivo_file.read()).decode()
            data["carta_aceptacion_filename"] = archivo_file.name

        try:
            # intento para quee Odoo no intente enviar correos
            context = {"mail_create_nosubscribe": True}
            estudiante_id = odoo.call(
                "tcu.estudiante",
                "create",
                args=[data],
                kwargs={"context": context}
            )

            success = f"Solicitud creada con ID: {estudiante_id}"
            return render(request, "solicitudes/nueva_solicitud.html", {
                "success": success, 
                "periodos": periodos, 
                "fecha_hoy": fecha_hoy
            })

        except Exception as e:
            error = f"Ocurrió un error: {e}"
            return render(request, "solicitudes/nueva_solicitud.html", {
                "error": error, 
                "periodos": periodos, 
                "fecha_hoy": fecha_hoy
            })

    return render(request, "solicitudes/nueva_solicitud.html", {
        "periodos": periodos, 
        "fecha_hoy": fecha_hoy
    })
