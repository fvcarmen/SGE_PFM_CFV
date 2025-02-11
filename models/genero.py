from odoo import api, models, fields

class Genero(models.Model):
    _name = 'cine_gestion.genero'
    _description = 'Género de contenido audiovisual'

    name = fields.Char(string="Nombre", required=True)  
    preferencia_horaria = fields.Boolean(string="Preferencia horaria")
    anuncios_ids = fields.One2many('cine_gestion.anuncio', 'genero_id', string="Anuncio")
    eventos_ids = fields.Many2many(
        'cine_gestion.evento',
        string="Evento",
    )


    _sql_constraints = [
        ('unique_name','unique(name)','El nombre del género debe ser único.')
    ]
    
    """@api.constrains('name')
    def _check_name(self):
        for record in self:
            if self.search([('name','=',record.name), ('id', '!=', record.id)]):
            raise ValidationError("El nombre del género debe ser único.")
    """