from odoo import api, models, fields

class Sala(models.Model):
    _name = "cine_gestion.sala"
    _description = "Salas de Cine"

    name = fields.Char("Nombre", required=True)
    filas =  fields.Integer("Cantidad de filas", required=True)
    columnas =  fields.Integer("Cantidad de columnas", required=True)
    capacidad = fields.Integer("Capacidad", compute="_capacidad_total")
    tamaño = fields.Char("Tipo de sala", compute="_size_sala")
    asientos_ids = fields.One2many('cine_gestion.asiento', 'sala_id', string="Asientos")
    sesiones_ids = fields.One2many('cine_gestion.sesion', 'sala_id', string="Sesiones")


    @api.depends("filas", "columnas")
    def _capacidad_total(self):
        for record in self:
            record.capacidad = record.filas * record.columnas

    @api.depends("capacidad")
    def _size_sala(self):
        for record in self:
            if record.capacidad > 100:
                record.tipo = "Mediana"
            elif record.capacidad >200:
                record.tipo = "Grande"
            else:
                record.tipo = "Pequeña"