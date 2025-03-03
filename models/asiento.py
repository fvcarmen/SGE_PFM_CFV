from odoo import api, models, fields

class Asiento(models.Model):
    _name = "cine_gestion.asiento"
    _description = "Asientos de sala"

    name = fields.Char("Nombre", compute="_compute_nombre_asiento")
    fila =  fields.Integer("Fila", required=True)
    columna =  fields.Integer("Columna", required=True)

    tipo = fields.Selection([
        ('NORM', 'Butaca normal'),
        ('MNSV', 'Butaca reservada minusvalía'),
        ('ESP', 'Butaca especial'),
        ], string="Tipo", default='NORM', required=True)
    
    sala_id = fields.Many2one('cine_gestion.sala', string="Sala")

    @api.depends('sala_id', 'fila', 'columna')
    def _compute_nombre_asiento(self):
        for asiento in self:
            if asiento.sala_id and asiento.fila and asiento.columna:
                asiento.name = f"{asiento.sala_id.name} Fila: {asiento.fila} Butaca: {asiento.columna}"
            else:
                asiento.name = "Asiento por asignar"