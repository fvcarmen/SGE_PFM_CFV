from odoo import models, fields

class Genero(models.Model):
    _name = 'cine_gestion.genero'
    _description = 'Género de contenido audiovisual'

    name = fields.Char(string="Nombre", required=True)  
    preferencia_horaria = fields.Boolean(string="Preferencia horaria")
    anuncios_ids = fields.One2many('cine_gestion.anuncio', 'genero_id', string="Anuncio")