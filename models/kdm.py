from odoo import models, fields, api

class Kdm(models.Model):
    _name = "cine_gestion.kdm"
    _description = "KDM (Key Delivery Message)"

    name = fields.Char(string="Clave", required=True)
    estado = fields.Boolean(string="Estado", default=True, required=True)
    vencimiento = fields.Date(string="Fecha de Vencimiento", required=True)
    evento_id = fields.Many2one('cine_gestion.evento', string="Evento", help="Evento al que pertenece")


    #actualizar todas las kdms que venzan 'hoy'
    @api.model
    def cron_actualizar_estado(self):
        today = fields.Date.context_today(self)
        kdms = self.search([('estado', '=', True), ('vencimiento', '<', today)])
        if kdms:
            kdms.write({'estado': False})