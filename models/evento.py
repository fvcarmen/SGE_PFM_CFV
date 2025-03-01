from odoo import models, fields

class Evento(models.Model):
    _name = "cine_gestion.evento"
    _description = "Eventos de Cine"

    name = fields.Char(string="Título", required=True)
    imagen = fields.Image(string="Imagen")
    es_pelicula = fields.Boolean(
        string="¿Se va a proyectar una película?",
        default=True
    )
    descripcion = fields.Text(string="Descripción")
    prioridad = fields.Selection(
        [
        ('5', 'Estreno'),
        ('4', 'Post-Estreno'),
        ('3', 'Normal'),
        ('2', 'Normal'),
        ('1', 'Baja Prioridad'),
        ('0', 'Sin prioridad'),
        ],
        default='5',
        #readonly=True,
        string="Prioridad"
    )
    
    activo = fields.Boolean(string="Activo", default=True)
    duracion = fields.Integer(string="Duración (min)", help="Duración en minutos", required=True)
    distribuidora = fields.Char(string="Distribuidora", required=True)
    kdms_ids = fields.One2many(
        'cine_gestion.kdm',
        'evento_id',
        string="KDM",
        help="Clave de KDM asociada"
    )
    pegi = fields.Selection(
        [
        ('desconocido', 'Desconocido'),
        ('tp', 'Todos los públicos'), 
        ('7', 'No recomendada para menores de 7 años'), 
        ('10', 'No recomendada para menores de 10 años'),
        ('13', 'No recomendada para menores de 13 años'),
        ('16', 'No recomendada para menores de 16 años'),
        ('18', 'No recomendada para menores de 18 años'),
        ],
        string="PEGI",
        default='desconocido',
        required=True
    )
    dcp = fields.Boolean(string="Formato DCP", default=False)
    generos_ids = fields.Many2many(
        'cine_gestion.genero',
        string="Género",
        required=True
    )
    sesiones_ids = fields.One2many(
        'cine_gestion.sesion',
        'evento_id',
        string="Sesiones"
    )

    

    """recaudacion_total = fields.Float(string="Recaudación Total", help="Ingresos generados")
    campo calculado a través de las entradas/tickets vendidos en cualquier sesion para el evento en concreto
    """
