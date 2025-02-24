from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta, time

class WizardGenerateSessions(models.TransientModel):
    """Wizard para solicitar los datos de generación de las sesiones"""
    _name = "cine_gestion.wizard_generate_sessions"
    _description = "Formulario de datos para la generación automática de sesiones"

    fecha_inicio = fields.Date(string="Fecha Inicio", required = True)
    fecha_final = fields.Date(string="Fecha Fin", required = True)
    hora_inicio = fields.Float(string="Hora de inicio primera sesión",required = True , help="Formato 24h: 18.50 = 18:30")
    hora_final = fields.Float(string="Hora de inicio última sesión",required = True , help="Formato 24h: 18.50 = 18:30")
    minimo_eventos = fields.Integer(string="Mínimo de eventos:", compute="_compute_minimo_eventos")
    listado_eventos = fields.Many2many(
        'cine_gestion.evento',
        string='Eventos',
        domain="[('activo','=', True)]",
    )
    listado_anuncios = fields.Many2many('cine_gestion.anuncio', string="Anuncios")
    listado_salas = fields.Many2many('cine_gestion.sala', string="Salas")
    listado_tarifas = fields.Many2many('cine_gestion.tarifa', string="Tarifas")

    #campo eventos mínimos calculado
    @api.depends('fecha_inicio', 'fecha_final', 'listado_salas', 'listado_eventos')
    def _compute_minimo_eventos(self):
        if self.fecha_inicio and self.fecha_final and self.listado_salas:
                # Calcular la cantidad de días entre las fechas
                dias = (self.fecha_final- self.fecha_inicio).days + 1
                # Calcular el mínimo de eventos (días * cantidad de salas)
                self.minimo_eventos = int((dias + len(self.listado_salas))*0.5)
        else:
                self.minimo_eventos = 0
    #restricción tarifas por tipo de día
    @api.constrains('listado_tarifas')
    def _check_unique_dia_valido(self):
        for record in self:
            dias_con_tarifa = []
            for tarifa in record.listado_tarifas:
                if tarifa.dia_valido in dias_con_tarifa:
                    raise UserError(f"Ya existe una tarifa con el código {tarifa.dia_valido}. No se permiten tarifas duplicadas para el mismo día." )
                dias_con_tarifa.append(tarifa.dia_valido)
                if tarifa.dia_valido == -1:
                    valor_default = True
            if not valor_default:
                raise UserError("Para evitar fallos de generación de sesiones, asigna al menos una tarifa con el valor -1")
            
            
    def generate_sessions(self):
        self.ensure_one()
        if not self.fecha_inicio or not self.fecha_final:
            raise UserError("Debes definir una fecha de inicio y una fecha de fin para la generación de sesiones.")
        if self.fecha_inicio > self.fecha_final:
            raise UserError("La fecha de inicio debe ser anterior a la fecha de fin para la generación de sesiones.")
        if self.hora_inicio >= self.hora_final:
            raise UserError("La hora de inicio debe ser anterior a la hora de fin para la generación de sesiones.")
        if not self.listado_eventos or self.minimo_eventos > len(self.listado_eventos): 
            raise UserError(f"Debes seleccionar al menos {self.minimo_eventos} evento/s para la generación de sesiones.")
        if not self.listado_salas:
            raise UserError("Debes seleccionar al menos una sala para la generación de sesiones.")
        if not self.listado_tarifas:
            raise UserError("Debes seleccionar al menos una tarifa válida para proceder con la generación de sesiones.")
        #quiero que la fecha fin y la fecha inicio solo tenga en cuenta el date y que haya otros 
        #2 campos que sean hora inicio y hora fin que gestionen hasta que hora pueden empezar las películas
        #widget="timesheet_uom_timer" campo float devuelve
        for sala in self.listado_salas:
            for evento in self.listado_eventos:

                hora_inicio = int(self.hora_inicio)
                minuto_inicio= int((self.hora_inicio- hora_inicio)*60)
                hora_final = int(self.hora_final) 

                minuto_final = int((self.hora_final - hora_final) * 60)
                fecha_final_generacion = datetime.combine(self.fecha_final, time(hora_final, minuto_final))
                fecha_sesion = datetime.combine(self.fecha_inicio, time(hora_inicio, minuto_inicio))

                duracion = evento.duracion + sum(anuncio.duracion for anuncio in self.listado_anuncios)

                while fecha_sesion <= (fecha_final_generacion + timedelta(minutes=duracion)):

                    if fecha_sesion.hour < hora_inicio or fecha_sesion.hour > hora_final:
                        fecha_sesion = fecha_sesion.replace(hour=hora_inicio, minute=minuto_inicio, second=0) + timedelta(days=1)
                        continue
                    
                    fecha_fin = fecha_sesion + timedelta(minutes=duracion)
                    
                    sesion_existente = self.env['cine_gestion.sesion'].search([
                        ('sala_id', '=', sala.id),
                        ('fecha_inicio', '<', fecha_fin),
                        ('fecha_fin', '>', fecha_sesion)
                    ])
                    sesion_solapada= self.env['cine_gestion.sesion'].search([
                        ('evento_id', '=', evento.id),
                        ('fecha_inicio', '=', fecha_sesion),
                        ('fecha_fin', '=', fecha_fin),
                    ])
                    if len(sesion_existente) == 0 and not sesion_solapada:
                        self.env['cine_gestion.sesion'].create({
                            'fecha_inicio': fecha_sesion,
                            'fecha_fin': fecha_fin,
                            'evento_id': evento.id,
                            'anuncios_ids': [(6, 0, self.listado_anuncios.ids)],
                            'sala_id': sala.id,
                            'tarifa_id': self.listado_tarifas and self.listado_tarifas[0].id or False
                        })

                    fecha_sesion += timedelta(minutes=duracion+20)

    
    