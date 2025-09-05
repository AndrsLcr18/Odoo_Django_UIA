from odoo import models, fields, api
from datetime import datetime

class TcuPeriodo(models.Model):
    _name = 'tcu.periodo'
    _description = 'Período de TCU'
    _order = 'anio desc, name'

    name = fields.Char('Nombre', required=True)
    activo = fields.Boolean('Activo', default=True)
    anio = fields.Selection('_get_year_selection', 'Año', required=True, default=lambda self: str(datetime.now().year))
    fecha_inicio = fields.Date('Fecha de Inicio', required=True)
    fecha_final = fields.Date('Fecha Final', required=True)

    # Relación con estudiantes
    tcu_estudiante_ids = fields.One2many('tcu.estudiante', 'periodo_id', string="Estudiantes")

    # Campos computados para estadísticas
    total_estudiantes = fields.Integer(
        'Total Estudiantes', compute='_compute_estudiantes_stats', store=True)
    estudiantes_aprobados = fields.Integer(
        'Estudiantes Aprobados', compute='_compute_estudiantes_stats', store=True)
    estudiantes_pendientes = fields.Integer(
        'Estudiantes Pendientes', compute='_compute_estudiantes_stats', store=True)

    @api.model
    def _get_year_selection(self):
        """Genera selección de años: actual + 4 siguientes"""
        current_year = datetime.now().year
        return [(str(current_year + i), str(current_year + i)) for i in range(5)]

    @api.depends('tcu_estudiante_ids.estado_solicitud')
    def _compute_estudiantes_stats(self):
        """Calcula estadísticas de estudiantes"""
        for record in self:
            record.total_estudiantes = len(record.tcu_estudiante_ids)
            record.estudiantes_aprobados = len(
                record.tcu_estudiante_ids.filtered(lambda x: x.estado_solicitud == 'aprobado'))
            record.estudiantes_pendientes = len(
                record.tcu_estudiante_ids.filtered(lambda x: x.estado_solicitud in ['en_revision', 'pendiente']))

    @api.constrains('fecha_inicio', 'fecha_final')
    def _check_fechas(self):
        """Valida que la fecha final sea posterior a la inicial"""
        for record in self:
            if record.fecha_final and record.fecha_inicio:
                if record.fecha_final <= record.fecha_inicio:
                    raise models.ValidationError(
                        'La fecha final debe ser posterior a la fecha de inicio.')
