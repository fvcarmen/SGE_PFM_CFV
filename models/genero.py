from odoo import api, models, fields

class Genero(models.Model):
    _name = 'cine_gestion.genero'
    _description = 'Género de contenido audiovisual'

    name = fields.Char(string="Nombre", required=True)  
    preferencia_horaria_inicio = fields.Datetime(string="Inicio preferencia horaria")
    preferencia_horaria_fin = fields.Datetime(string="Fin preferencia horaria")

    anuncios_ids = fields.One2many(
        'cine_gestion.anuncio',
        'genero_id',
        string="Anuncio"
        )
    
    eventos_ids = fields.Many2many(
        'cine_gestion.evento',
        string="Evento",
    )
    
    #nombre de género único
    _sql_constraints = [
        ('unique_name','unique(name)','El nombre del género debe ser único.')
    ]