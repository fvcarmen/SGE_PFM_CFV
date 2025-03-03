from datetime import timedelta, date, datetime
from odoo import api, models, fields
class Sesion(models.Model):
    _name = "cine_gestion.sesion"
    _description = "Sesiones de Cine"
    
    name = fields.Char(string="Nombre", compute="_compute_session_name", store=True)
    fecha_inicio = fields.Datetime(string="Fecha de Inicio", required=True, store=True)
    fecha_fin = fields.Datetime(string="Fecha de Fin", compute="_compute_fecha_fin", store = True)
    duracion = fields.Integer(string="Duración (min)", compute="_compute_duracion", store=True)
    ocupacion = fields.Integer(string="Ocupación", default=0)
    activo = fields.Boolean(string="Activo", default=True)

    anuncios_ids = fields.Many2many('cine_gestion.anuncio', string="Anuncios")
    evento_id = fields.Many2one('cine_gestion.evento', string="Evento", required=True)

    sala_id = fields.Many2one(
        'cine_gestion.sala',
        string="Sala",
        help="Sala en la que se proyecta",
        required=True
        )
    
    tarifa_id = fields.Many2one(
        'cine_gestion.tarifa',
        string="Tarifa",
        required=True
        )
    
    estado_kdm = fields.Char(string="Estado", compute="_compute_estado_kdm")
    kdms = fields.One2many('cine_gestion.kdm', 'evento_id', string ="KDMS", related="evento_id.kdms_ids")

    #función para comprobar si la sesión programada tendrá un kdm válido
    @api.depends('fecha_fin', 'kdms')
    def _compute_estado_kdm(self):
        for sesion in self:
            if self.fecha_fin:
                fecha_fin = datetime.date(self.fecha_fin)

                kdm_validos = self.kdms.filtered(
                    lambda kdm: kdm.vencimiento > fecha_fin
                )

                if not kdm_validos:
                    self.estado_kdm = "KDM inválido"
                else:
                    self.estado_kdm=""
            else:
                self.estado_kdm=""

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
                if sesion.evento_id.name and sesion.sala_id.name:
                    sesion.name=f"{sesion.sala_id.name}: {sesion.evento_id.name} del {sesion.fecha_inicio}"
                else:
                    sesion.name="Sesión por Asignar"
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
    

