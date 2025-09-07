# Proyecto TCU UIA - Odoo + Django

##  Descripción
Este proyecto integra **Odoo 17** y **Django 5** para gestionar el **Trabajo Comunal Universitario (TCU)** en la UIA.  
El objetivo es que los estudiantes puedan realizar solicitudes desde una aplicación en Django, mientras que Odoo centraliza la gestión académica y administrativa.

---

## 📂 Estructura del Repositorio

##  Estructura del módulo

1)modules/tcu_manager/
│── init.py
│── manifest.py # Metadatos del módulo
│
├── controllers/ # Controladores para exponer APIs
│ └── tcu_controller.py
│
├── models/ # Modelos de datos de Odoo
│
├── security/ # Archivos de reglas de acceso
│
├── views/ # Vistas XML (formularios, árboles, menús)
│
├── data/ # Datos iniciales (si aplica)
├── demo/ # Datos demo (si aplica)
│
└── static/description/ # Información para Apps de Odoo
└── index.html

2)TCU_DJANGO
├── tcu_django/ # Proyecto Django (frontend + integración con Odoo)
│ ├── solicitudes/ # Aplicación Django
│ └── tcu_django/ # Configuración principal del proyecto


## ⚙️ Instalación

### 🔹 Requisitos
- Python 3.11+
- PostgreSQL 15+
- Odoo 17
- Django 5
- Pipenv o venv (recomendado)

---

### 🔹 Configuración de Odoo
1. Instalar Odoo 17 y crear la base de datos correspondiente.
2. Copiar el módulo `tcu_manager` dentro de `addons` o en un directorio personalizado:
   ```ini
   addons_path = modules,odoo/addons
3.Reiniciar el servidor de Odoo.

4.Activar el modo desarrollador.

5.Actualizar la lista de aplicaciones e instalar TCU Manager.

### 🔹 Configuración de Django
Acceder al directorio tcu_django:

Paso 1 : 
cd tcu_django
Instalar dependencias:

Paso 2 :
pip install -r requirements.txt


Paso 3 :
Aplicar migraciones:
python manage.py migrate
Ejecutar el servidor:

Paso 4 :
python manage.py runserver


-------------------------------------------------
### 🔹  Funcionalidades:

###  🔹 Odoo (Módulo tcu_manager)

-Modelos para estudiantes y solicitudes de TCU.


-Vistas en Odoo para gestión administrativa.

-Seguridad con reglas de acceso.

------------------------------------------------
### 🔹 Django (tcu_django)
-Formulario para búsqueda de estudiantes.

-Creación de solicitudes de TCU.

-Consumo de APIs expuestas por Odoo.

-Interfaz amigable para estudiantes.

-----------------------------------------------
### 🔹 Integración Odoo ↔ Django

Django los consume desde tcu_django/solicitudes/odoo_rpc.py.

Flujo:

Estudiante busca su información en Django.

Django consulta Odoo vía API.

Odoo responde con los datos del estudiante y estado de la solicitud.

El usuario puede crear o dar seguimiento a su solicitud.
------------------------------------------------
### 📖 Autor
Andrés Serrano Cajina
📅 Proyecto TCU - UIA
-Vistas en Odoo para gestión interna.
