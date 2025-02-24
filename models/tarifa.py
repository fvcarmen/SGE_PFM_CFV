from odoo import models, fields, api
from odoo.exceptions import UserError

class Tarifas(models.Model):
    _name = "cine_gestion.tarifa"
    _description = "Tarifa"

    name = fields.Char(string="Nombre", required=True)
    precio = fields.Float(string="Precio", required=True)
    dia_valido = fields.Integer(string="Día aplicable (-1 a 6)", help="-1 = tarifa default, 0 = Lunes ... 6 = Domingo", default = -1)
    descuentos_ids = fields.One2many('cine_gestion.descuento', 'tarifa_id', string="Descuentos")
    sesiones_ids = fields.One2many('cine_gestion.sesion', 'tarifa_id', string = "Sesiones")

    @api.constrains('dia_valido')
    def _comprobar_dia_valido(self):
        for record in self:
            if record.dia_valido is None or record.dia_valido < -1 or record.dia_valido > 6:
                raise UserError("Debes seleccionar un día válido (entre -1 y 6).")