# -*- coding: utf-8 -*-
{
    'name': 'tcu_manager',
    'version': '1.0.0',
    'category': 'Education',
    'summary': 'Módulo para control y registro de estudiantes de TCU',
    'description': """
        Módulo para gestionar:
        - Períodos de TCU
        - Estudiantes de TCU
        - Control de solicitudes
        - Notificaciones por correo
    """,
    'author': 'Andres Serrano Cajina',
    'website': 'https://www.linkedin.com/in/andr%C3%A9s-serrano-cajina-026183139/',
    'depends': ['base', 'mail','web','website'],
    'data': [
        'security/ir.model.access.csv',
        'views/tcu_periodo_views.xml',
        'views/tcu_estudiante_views.xml',
        'views/tcu_menu_views.xml',
        'data/mail_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',  

}