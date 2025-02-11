from odoo import api, models, fields
class Sesion(models.Model):
    _name = "cine_gestion.sesion"
    _description = "Sesiones de Cine"
    
    name = fields.Char(string="Nombre")
    fecha_inicio = fields.Datetime(string="Fecha de Inicio", required=True)
    fecha_fin = fields.Datetime(string="Fecha de Fin", required=True) #calculada según la duración??¿?¿?¿? y la fecha de inicio=?=?=?=
    evento_id = fields.Many2one('sesiones_ids', string="Evento", required=True)
    duracion = fields.Integer(string="Duración (min)", compute="_compute_duracion", store=True)
    ocupacion = fields.Integer(string="Ocupación", default=0)
    anuncios_ids = fields.Many2many('cine_gestion.anuncio', string="Anuncios")
    sala_id = fields.Many2one(
        'cine_gestion.sala',
        string="Sala",
        help="Sala en la que se proyecta",
        required=True
        )
    
    @api.depends('anuncios_ids')
    def _compute_duracion(self):
        for sesion in self:
            duracion = 0
            for anuncio in sesion.anuncios_ids:
                sesion.duracion = duracion + anuncio.duracion
    #campo calculado de la duración
    

