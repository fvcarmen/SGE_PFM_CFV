from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Evento(models.Model):
    _name = "cine_gestion.evento"
    _description = "Eventos de Cine"

    name = fields.Char(string="Título", required=True)
    descripcion = fields.Text(string="Descripción")
    activo = fields.Boolean(string="Activo", default=True)
    duracion = fields.Integer(string="Duración (min)", help="Duración en minutos", required=True)
    dcp = fields.Boolean(string="Formato DCP", default=False)
    distribuidora = fields.Char(string="Distribuidora", required=True)

    imagen = fields.Image(string="Imagen")
    es_pelicula = fields.Boolean(
        string="¿Se va a proyectar una película?",
        default=True
    )

    prioridad = fields.Selection(
        [
        ('5', 'Prioridad Estreno'),
        ('4', 'Prioridad Post-Estreno'),
        ('3', 'Prioridad Alta'),
        ('2', 'Prioridad Normal'),
        ('1', 'Baja Prioridad'),
        ('0', 'Sin prioridad'),
        ],
        default='5',
        required=True,
        string="Prioridad"
    )
    
    kdms_ids = fields.One2many(
        'cine_gestion.kdm',
        'evento_id',
        string="KDM",
        help="Clave de KDM asociada"
    )

    tiene_kdm_activo = fields.Boolean(
        string="Tiene KDM Activo",
        compute="_compute_tiene_kdm_activo",
        store=True
    )

    pegi = fields.Selection(
        [
        ('desconocido', 'Desconocido'),
        ('tp', 'Todos los públicos'), 
        ('7', 'No recomendada para menores de 7 años'), 
        ('10', 'No recomendada para menores de 10 años'),
        ('13', 'No recomendada para menores de 13 años'),
        ('16', 'No recomendada para menores de 16 años'),
        ('18', 'No recomendada para menores de 18 años'),
        ],
        string="PEGI",
        default='desconocido',
        required=True
    )
    
    generos_ids = fields.Many2many(
        'cine_gestion.genero',
        string="Género",
        required=True
    )

    sesiones_ids = fields.One2many(
        'cine_gestion.sesion',
        'evento_id',
        string="Sesiones",
        readonly=True
    )

    @api.depends('kdms_ids.estado')
    def _compute_tiene_kdm_activo(self):

        for rec in self:
            rec.tiene_kdm_activo = any(kdm.estado for kdm in rec.kdms_ids)


    def actualizar_campo_semanalmente(self):

        """Método que se ejecuta cada semana para actualizar registros activos"""
        _logger.info("CRON ejecutado: actualizando eventos")
        registros = self.search([('activo', '=', True)])
        for record in registros:
            if len(record.sesiones_ids) > 1:
                record.write({
                    'prioridad': str(int(record.prioridad)-1),
                })
            if int(record.prioridad) < 0:
                record.write({
                    'activo': False,
                })
        _logger.info("CRON ejecutado: campo 'prioridad' actualizado para %s registros activos.", len(registros))

