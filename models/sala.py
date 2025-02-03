from odoo import api, models, fields

class Sala(models.Model):
    _name = "cine_gestion.sala"
    _description = "Salas de Cine"

    name = fields.Char("Nombre", required=True)
    filas =  fields.Integer("Cantidad de filas", required=True)
    columnas =  fields.Integer("Cantidad de columnas", required=True)
    capacidad = fields.Integer("Capacidad", compute="_capacidad_total")
    asientos_ids = fields.One2many('cine_gestion.asiento', 'sala_id', string="Asientos")

    @api.depends("filas", "columnas")
    def _capacidad_total(self):
        for record in self:
            record.capacidad = record.filas * record.columnas
    #1 sala tiene relacion con 0 o varias sesiones