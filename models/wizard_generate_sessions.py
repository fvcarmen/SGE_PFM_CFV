from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class WizardGenerateSessions(models.TransientModel):
    """Wizard para solicitar los datos de generación de las sesiones"""
    _name = "cine_gestion.wizard_generate_sessions"
    _description = "Formulario de datos para la generación automática de sesiones"

    fecha_inicio = fields.Datetime(string="Fecha Inicio")
    fecha_final = fields.Datetime(string="Fecha Fin")
    minimo_eventos = fields.Integer(string="Mínimo de eventos:", compute="_compute_minimo_eventos")
    listado_eventos = fields.Many2many(
        'cine_gestion.evento',
        string='Eventos',
        domain="[('activo','=', True)]",
    )
    listado_anuncios = fields.Many2many('cine_gestion.anuncio', string="Anuncios")
    listado_salas = fields.Many2many('cine_gestion.sala', string="Salas")
    listado_tarifas = fields.Many2many('cine_gestion.tarifa', string="Tarifas")

    @api.depends('fecha_inicio', 'fecha_final', 'listado_salas', 'listado_eventos')
    def _compute_minimo_eventos(self):
        if self.fecha_inicio and self.fecha_final and self.listado_salas:
                # Calcular la cantidad de días entre las fechas
                dias = (self.fecha_final.date().days - self.fecha_inicio.date()).days + 1
                # Calcular el mínimo de eventos (días * cantidad de salas)
                self.minimo_eventos = dias * len(self.listado_salas)
        else:
                self.minimo_eventos = 0
    #olvidate de la fecha que me preocupa poco
    #meter un botón en el wizard no vale que lo genere por defecto, generar la vista del wizard
    #con los campos de arriba y un footer con un botón que ejecute el código de abajo (generate_sessions())
    #que funcione eso
    #conseguir los datos necesarios para aplicar la lógica, conseguir los datos (son únicos?)self.ensure_one
    #self.fecha_inicio, self.fecha_final, self.listado_eventos, comprobación de errores, buscar características
    #operar mirar qué hace falta
    def generate_sessions(self):
        self.ensure_one()
        if not self.fecha_inicio or not self.fecha_final:
            raise UserError("Debes definir una fecha de inicio y una fecha de fin para la generación de sesiones.")
        if self.fecha_inicio >= self.fecha_final:
            raise UserError("La fecha de inicio debe ser anterior a la fecha de fin para la generación de sesiones.")
        """or len(self.listado_eventos) < self.minimo_eventos?"""
        if not self.listado_eventos: 
            raise UserError(f"Debes seleccionar al menos evento para la generación de sesiones.")
        if not self.listado_salas:
            raise UserError("Debes seleccionar al menos una sala para la generación de sesiones.")
        if not self.listado_tarifas:
            raise UserError("Debes seleccionar al menos una tarifa para proceder con la generación de sesiones.")
        """
        evento = self.listado_eventos[0]  
        sala = self.listado_salas[0]  
        tarifa = self.listado_tarifas[0]  

        valores_sesion = {
            'fecha_inicio': self.fecha_inicio,
            'evento_id': evento.id,
            'sala_id': sala.id,
            'tarifa_id': tarifa.id,
            'ocupacion': 0,  
            'anuncios_ids': [(6, 0, [anuncio.id for anuncio in self.listado_anuncios])],  
        }
        self.env['cine_gestion.sesion'].create(valores_sesion)
        """
        #widget="timesheet_uom_timer" campo float devuelve
        for sala in self.listado_salas:
            for evento in self.listado_eventos:
                fecha_sesion = self.fecha_inicio
                while fecha_sesion <= self.fecha_final:
                    duracion = evento.duracion + sum(anuncio.duracion for anuncio in self.listado_anuncios)
                    fecha_fin = fecha_sesion + timedelta(minutes=duracion)
                    sesion_existente = self.env['cine_gestion.sesion'].search([
                        ('sala_id', '=', sala.id),
                        ('fecha_inicio', '<', fecha_fin),
                        ('fecha_fin', '>', fecha_sesion)
                    ])
                    if len(sesion_existente) == 0:
                        self.env['cine_gestion.sesion'].create({
                            'fecha_inicio': fecha_sesion,
                            'evento_id': evento.id,
                            'duracion': duracion,
                            'anuncios_ids': [(6, 0, self.listado_anuncios.ids)],
                            'sala_id': sala.id,
                            'tarifa_id': self.listado_tarifas and self.listado_tarifas[0].id or False
                        })
                    fecha_sesion += timedelta(minutes=duracion)
    