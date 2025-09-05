from odoo import models, fields, api
from odoo.exceptions import UserError

class TcuEstudiante(models.Model):
    _name = 'tcu.estudiante'
    _description = 'Estudiante de TCU'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Información del estudiante
    name = fields.Char('Nombre Completo', required=True, tracking=True)
    identificacion = fields.Char('Identificación', required=True, tracking=True)
    carnet = fields.Char('Carnet', required=True, tracking=True)
    correo = fields.Char('Correo Electrónico', required=True, tracking=True)
    telefono = fields.Char('Teléfono', tracking=True)
    
    # Control de solicitud
    periodo_id = fields.Many2one('tcu.periodo', 'Período de TCU', required=True, tracking=True)
    lugar_tcu = fields.Char('Lugar de TCU', tracking=True)
    encargado_estudiante = fields.Char('Encargado del Estudiante', tracking=True)
    fecha_solicitud = fields.Date('Fecha de Solicitud', default=fields.Date.context_today, tracking=True)
    estado_solicitud = fields.Selection([
        ('en_revision', 'En Revisión'),
        ('pendiente', 'Pendiente'),
        ('rechazado', 'Rechazado'),
        ('aprobado', 'Aprobado')
    ], 'Estado de Solicitud', default='en_revision', tracking=True)
    
    observaciones = fields.Text('Observaciones', tracking=True)
    motivo_estado = fields.Text('Motivo del Estado')
    
    # Documentos
    carta_aceptacion = fields.Binary('Carta de Aceptación')
    carta_aceptacion_filename = fields.Char('Nombre del Archivo')
    
    # Control de campos readonly
    campos_readonly = fields.Boolean('Campos Solo Lectura', default=True)
    
    # Campo computado para mostrar estado con colores
    estado_display = fields.Html('Estado', compute='_compute_estado_display', store=False)

    @api.depends('estado_solicitud')
    def _compute_estado_display(self):
        colores = {
            'en_revision': '#17a2b8',  
            'pendiente': '#ffc107',    
            'rechazado': '#dc3545',    
            'aprobado': '#28a745'      
        }
        for record in self:
            color = colores.get(record.estado_solicitud, '#6c757d')
            estado_text = dict(record._fields['estado_solicitud'].selection)[record.estado_solicitud]
            record.estado_display = f'<span style="color: {color}; font-weight: bold;">●</span> {estado_text}'

    @api.onchange('estado_solicitud')
    def _onchange_estado_solicitud(self):
        if self.estado_solicitud in ['pendiente', 'rechazado']:
            if not self.motivo_estado:
                return {
                    'warning': {
                        'title': 'Motivo Requerido',
                        'message': 'Debe indicar el motivo para el estado pendiente o rechazado.'
                    }
                }

    def action_habilitar_edicion(self):
        """Acción para habilitar la edición manual de campos"""
        self.write({'campos_readonly': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_deshabilitar_edicion(self):
        """Acción para deshabilitar la edición (volver a readonly)"""
        self.write({'campos_readonly': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_enviar_notificacion_correo(self):
        """Acción para enviar notificación por correo del estado"""
        if not self.correo:
            raise UserError('El estudiante no tiene correo registrado.')
        
        template = self.env.ref('tcu_module.mail_template_estado_solicitud', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)
            self.message_post(
                body=f'Notificación enviada por correo a {self.correo}',
                message_type='notification'
            )
        else:
            self.message_post(
                body=f'Template de correo no encontrado',
                message_type='notification'
            )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Correo Enviado',
                'message': f'Notificación enviada exitosamente a {self.correo}',
                'type': 'success'
            }
        }

    @api.model
    def create(self, vals):
        """Override create para logging"""
        estudiante = super(TcuEstudiante, self).create(vals)
        estudiante.message_post(
            body=f'Nuevo estudiante registrado para TCU: {estudiante.name}',
            message_type='notification'
        )
        return estudiante

    @api.constrains('correo')
    def _check_email(self):
        for record in self:
            if record.correo and '@' not in record.correo:
                raise models.ValidationError('Formato de correo inválido.')

    @api.constrains('carnet', 'periodo_id')
    def _check_carnet_unique(self):
        for record in self:
            if record.carnet and record.periodo_id:
                existing = self.search([
                    ('carnet', '=', record.carnet),
                    ('periodo_id', '=', record.periodo_id.id),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise models.ValidationError(f'Ya existe un estudiante con carnet {record.carnet} en el período {record.periodo_id.name}.')