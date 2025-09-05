# # -*- coding: utf-8 -*- ESTO SE DESCARTA YA QUE NO SE USO
# from odoo import http
# from odoo.http import request
# import logging

# _logger = logging.getLogger(__name__)
# _logger.info(">>> tcu_controller.py ejecutado <<<")

# class TCUController(http.Controller):

#     @http.route('/api/get_estudiante', type='json', auth='public', csrf=False, methods=['POST'])
#     def get_estudiante(self, identificacion=None):
#         if not identificacion:
#             return {'success': False, 'message': 'Identificación requerida'}

#         estudiante = request.env['tcu.estudiante'].sudo().search(
#             [('identificacion', '=', identificacion)], limit=1
#         )
#         if not estudiante:
#             return {'success': False, 'message': 'Estudiante no encontrado'}

#         return {
#             'success': True,
#             'data': {
#                 'name': estudiante.name,
#                 'carnet': estudiante.carnet,
#                 'correo': estudiante.email,
#                 'estado': estudiante.estado_solicitud
#             }
#         }

#     @http.route('/api/get_periodo', type='json', auth='public', csrf=False, methods=['POST'])
#     def get_periodo(self):
#         periodos = request.env['tcu.periodo'].sudo().search([('activo', '=', True)])
#         data = [{'id': p.id, 'nombre': p.name} for p in periodos]
#         return {'success': True, 'data': data}

#     @http.route('/api/validar_estado', type='json', auth='public', csrf=False, methods=['POST'])
#     def validar_estado(self, identificacion=None):
#         if not identificacion:
#             return {'success': False, 'message': 'Identificación requerida'}

#         estudiante = request.env['tcu.estudiante'].sudo().search(
#             [('identificacion', '=', identificacion)], limit=1
#         )
#         if not estudiante:
#             return {'success': False, 'message': 'Estudiante no encontrado'}

#         return {'success': True, 'estado': estudiante.estado_solicitud}

#     @http.route('/api/crear_solicitud', type='json', auth='public', csrf=False, methods=['POST'])
#     def crear_solicitud(self, **kwargs):
#         data = kwargs.get('data')
#         if not data or 'identificacion' not in data:
#             return {'success': False, 'message': 'Datos incompletos'}

#         try:
#             estudiante = request.env['tcu.estudiante'].sudo().search(
#                 [('identificacion', '=', data.get('identificacion'))], limit=1
#             )

#             if not estudiante:
#                 return {'success': False, 'message': 'Estudiante no encontrado'}

#             solicitud = request.env['tcu.solicitud'].sudo().create({
#                 'estudiante_id': estudiante.id,
#                 'observaciones': data.get('observaciones', ''),
#                 'archivo': data.get('archivo') or False
#             })

#             estudiante.sudo().write({'estado_solicitud': 'pendiente'})
#             _logger.info(f"Solicitud TCU creada para estudiante {estudiante.name} (ID: {solicitud.id})")

#             return {'success': True, 'solicitud_id': solicitud.id}

#         except Exception as e:
#             _logger.error(f"Error al crear solicitud: {str(e)}")
#             return {'success': False, 'message': 'Error interno al crear la solicitud'}
