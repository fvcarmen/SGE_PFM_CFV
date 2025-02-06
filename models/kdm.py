from odoo import models, fields

class Kdm(models.Model):
    _name = "cine_gestion.kdm"
    _description = "KDM (Key Delivery Message)"

    name = fields.Char(string="Clave", required=True)
    estado = fields.Boolean(string="Estado", default=True)
    vencimiento = fields.Date(string="Fecha de Vencimiento")
    evento_id = fields.Many2one('cine_gestion.evento', string="Evento", help="Evento al que pertenece")