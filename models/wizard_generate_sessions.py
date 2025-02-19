from odoo import models, fields


class WizardGenerateSessions(models.TransientModel):
    """Wizard para solicitar los datos de generación de las sesiones"""
    _name = "cine_gestion.wizard_generate_sessions"
    _description = "Formulario de datos para la generación automática de sesiones"

    fecha_inicio = fields.Datetime(string="Fecha Inicio")
    fecha_final = fields.Datetime(string="Fecha Fin")
    nombre = fields.Char(string="Nombre", default="")

    def generate_sessions(self):
        pass