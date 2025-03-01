from odoo import models, fields, api
from odoo.exceptions import UserError

class Tarifas(models.Model):
    _name = "cine_gestion.tarifa"
    _description = "Tarifa"

    name = fields.Char(string="Nombre", required=True)
    precio = fields.Float(string="Precio", required=True)
    #lista checkbox odoo (xml widget="many2many_checkboxes")
    dia_tarifa = fields.Integer(string="Día aplicable (-1 a 6)", help="-1 = tarifa default, 0 = Lunes ... 6 = Domingo", default = -1)
    descuentos_ids = fields.One2many('cine_gestion.descuento', 'tarifa_id', string="Descuentos")
    sesiones_ids = fields.One2many('cine_gestion.sesion', 'tarifa_id', string = "Sesiones")
    activo = fields.Boolean(string="Activo", default=True)
    @api.constrains('dia_tarifa')
    def _comprobar_dia_tarifa(self):
        for record in self:
            if record.dia_tarifa is None or record.dia_tarifa < -1 or record.dia_tarifa > 6:
                raise UserError("Debes seleccionar un día válido (entre -1 y 6).")