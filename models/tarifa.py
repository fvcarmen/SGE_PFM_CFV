from odoo import models, fields

class Tarifas(models.Model):
    _name = "cine_gestion.tarifa"
    _description = "Tarifa"

    name = fields.Char(string="Nombre", required=True)
    precio = fields.Float(string="Precio", required=True)
    descuentos_ids = fields.One2many('cine_gestion.descuento', 'tarifa_id', string="Descuentos")
