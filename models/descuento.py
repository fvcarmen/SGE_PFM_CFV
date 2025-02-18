from odoo import models, fields

class Descuento(models.Model):
    _name = "cine_gestion.descuento"
    _description = "Descuentos"

    name = fields.Char(string="Nombre", required=True)
    descuento = fields.Integer(string="Descuento a aplicar", help="Número entero del 1 al 100", required=True)
    tarifa_id = fields.Many2one('cine_gestion.tarifa', string="Tarifa")