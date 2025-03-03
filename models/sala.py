from odoo import api, models, fields

class Sala(models.Model):
    _name = "cine_gestion.sala"
    _description = "Salas de Cine"

    name = fields.Char("Nombre", required=True)
    filas =  fields.Integer("Cantidad de filas", required=True)
    columnas =  fields.Integer("Cantidad de columnas", required=True)
    capacidad = fields.Integer("Capacidad", compute="_capacidad_total")
    tipo = fields.Char("Tipo de sala", compute="_compute_size")
    activo = fields.Boolean(string="Activo", default=True)

    asientos_ids = fields.One2many('cine_gestion.asiento', 'sala_id', string="Asientos")
    sesiones_ids = fields.One2many('cine_gestion.sesion', 'sala_id', string="Sesiones")
    

    #función calculo capacidad
    @api.depends("filas", "columnas")
    def _capacidad_total(self):
        for sala in self:
            sala.capacidad = sala.filas * sala.columnas


    #función tipo de sala
    @api.depends('capacidad')
    def _compute_size(self):
        for sala in self:
            if sala.capacidad > 200:
                sala.tipo = "Grande"
            elif sala.capacidad > 100:
                sala.tipo = "Mediana"
            else:
                sala.tipo = "Pequeña"