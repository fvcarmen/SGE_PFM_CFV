from odoo import api, models, fields

class Asiento(models.Model):
    _name = "cine_gestion.asiento"
    _description = "Asientos de sala"

    name = fields.Char("Nombre")
    fila =  fields.Integer("Fila", required=True)
    columna =  fields.Integer("Columna", required=True)
    tipo = fields.Selection([
        ('NORM', 'Butaca normal'),
        ('MNSV', 'Butaca reservada minusvalía'),
        ('ESP', 'Butaca especial'),
        ], string="Tipo", default='NORM', required=True)
    sala_id = fields.Many2one('cine_gestion.sala', string="Sala")