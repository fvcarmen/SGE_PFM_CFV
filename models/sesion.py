from datetime import timedelta
from odoo import api, models, fields
class Sesion(models.Model):
    _name = "cine_gestion.sesion"
    _description = "Sesiones de Cine"
    
    name = fields.Char(string="Nombre", compute="_compute_session_name", store = True)
    fecha_inicio = fields.Datetime(string="Fecha de Inicio", required=True)
    fecha_fin = fields.Datetime(string="Fecha de Fin", compute="_compute_fecha_fin", required=True, store = True)
    evento_id = fields.Many2one('cine_gestion.evento', string="Evento", required=True)
    duracion = fields.Integer(string="Duración (min)", compute="_compute_duracion", store=True)
    ocupacion = fields.Integer(string="Ocupación", default=0)
    anuncios_ids = fields.Many2many('cine_gestion.anuncio', string="Anuncios")
    sala_id = fields.Many2one(
        'cine_gestion.sala',
        string="Sala",
        help="Sala en la que se proyecta",
        required=True
        )
    tarifa_id = fields.Many2one('cine_gestion.tarifa', string="Tarifa")
    #vista lista que aparezca ya agrupada por grupos (día y luego salas) 
    #que muestre la hora fin, la duración, la ocupación y la tarifa (correo)
    
    #función para calcular la duración de la sesión
    @api.depends('anuncios_ids', 'evento_id')
    def _compute_duracion(self):
        for sesion in self:
            duracion = sesion.evento_id.duracion if sesion.evento_id else 0
            for anuncio in sesion.anuncios_ids:
                duracion = duracion + anuncio.duracion
            sesion.duracion = duracion
    
    #función para calcular el nombre de la sesión
    @api.depends('fecha_inicio', 'evento_id', 'sala_id')
    def _compute_session_name(self):
        for sesion in self:
            if sesion.fecha_inicio and sesion.evento_id and sesion.sala_id:
                sesion.name=f"{sesion.sala_id.name}: {sesion.evento_id.name} del {sesion.fecha_inicio}"
            else:
                sesion.name="Sesión por Asignar"
    
    #función para calcular la fecha fin de la sesión
    @api.depends('fecha_inicio', 'duracion')
    def _compute_fecha_fin(self):
        for sesion in self:
            if sesion.fecha_inicio and sesion.duracion:
                sesion.fecha_fin = sesion.fecha_inicio + timedelta(minutes=sesion.duracion)
            else:
                sesion.fecha_fin = sesion.fecha_inicio 
    

