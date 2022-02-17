# -*- coding: utf-8 -*-

from typing import Tuple
from odoo import models, fields, api, exceptions

class Electricidad( models.Model):
    _inherit = 'account.move'
    linea_electricidad = fields.One2many(
        comodel_name="linea.servicio", 
        inverse_name="move_id",
        states={'draft': [('readonly', False)]})
    
    subtotal_electricidad = fields.Float( string="Subtotal Electricidad", store=True)
    #-------------- SECCION DE CONSUMO ----------------------------
    lectura_actual = fields.Integer( string = "Lectura Actual", store=True)
    lectura_anterior = fields.Integer( string = "Lectura Anterior", store=True)
    factor_multiplicador = fields.Integer( string = "Factor Multiplicador", store=True)
    cantidad_medida = fields.Integer( string = "Cantidad Medida")
    kwh_equivalente = fields.Float( string = "kwh Equivalente")
    monto_total_consumo = fields.Float( string = "Monto total consumo", store=True)

    #-------------- SECCION DE DEMANDA ---------------------------
    demanda_asignada = fields.Integer( string = "Demanda asignada", store=True)
    demanda_leida = fields.Integer( string = "Demanda Leida", store=True)
    demanda_facturada = fields.Integer( string = "Demanda Facturada", store=True)
    monto_total_demanda = fields.Float( string = "Monto total demanda", store=True)

    @api.onchange('lectura_actual','lectura_anterior','factor_multiplicador','dias_lectura')
    def _compute_cantidad_medida( self):
        for record in self:
            if record.lectura_actual and record.lectura_anterior and record.factor_multiplicador and record.dias_lectura:
                record.cantidad_medida = ( record.lectura_actual - record.lectura_anterior) * record.factor_multiplicador
                linea_combustible = self.linea_electricidad.search([['clasificacion','=','combustible']])
                linea_combustible.write(
                    {
                        'cantidad': record.cantidad_medida,
                        'subtotal': record.cantidad_medida * linea_combustible.precio_unidad
                    }
                )
                if (record.dias_lectura > 0):
                    record.kwh_equivalente = (record.cantidad_medida * 30) / record.dias_lectura            
