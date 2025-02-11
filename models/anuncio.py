from odoo import api, models, fields

class Anuncio(models.Model):
    _name = "cine_gestion.anuncio"
    _description = "Anuncios"
    name = fields.Char(string="Nombre")
    duracion = fields.Integer(string="Duración (min)", help="Duración en minutos", required=True, default='0')
    pegi = fields.Selection([
        ('DESC', 'Desconocido'),
        ('tp', 'Todos los públicos'), 
        ('7', 'No recomendada para menores de 7 años'), 
        ('10', 'No recomendada para menores de 10 años'),
        ('13', 'No recomendada para menores de 13 años'),
        ('16', 'No recomendada para menores de 16 años'),
        ('18', 'No recomendada para menores de 18 años'),
        ], string="PEGI", default='DESC', required=True)
    genero_id = fields.Many2one('cine_gestion.genero', string="Género")
    sesiones_ids = fields.Many2many('cine_gestion.sesion', string="Sesiones")