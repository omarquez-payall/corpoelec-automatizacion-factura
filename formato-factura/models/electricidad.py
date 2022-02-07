# -*- coding: utf-8 -*-

from typing import Tuple
from odoo import models, fields, api, exceptions

class Electricidad( models.Model):
    _inherit = 'account.move'
    #_name = "servicio.electricidad"
    #_description = "Modelo creado para el detalle del servicio de electricidad"

    #-------------- FACTURA ---------------------------------------
    #lineas_detalle = fields.
    #factura_id = fields.Many2one(
    #    comodel_name = "account.move"
    #)
    #dias_lectura = fields.Integer( string ="Dias Lectura", related ="factura_id.dias_lectura")
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
                    self._compute_tarifa_consumo_lines()
            

    @api.onchange('monto_total_consumo')
    def _compute_tarifa_consumo_lines(self):
        if ( self.monto_total_consumo >0):
            linea_consumo = self.linea_electricidad.search([['clasificacion','=','consumo']])
            tarifa = ( self.monto_total_consumo / self.dias_lectura) * (30 / self.kwh_equivalente)
            linea_consumo.write(
                {
                    'cantidad': self.kwh_equivalente,
                    'precio_unidad':tarifa,
                    'subtotal': self.kwh_equivalente * tarifa
                }
            )
            self._onchange_subtotal()

    @api.onchange('monto_total_demanda')
    def _compute_tarifa_demanda_lines(self):
        if (self.monto_total_demanda >0):
            demanda_equivalente = 0
            if ( self.demanda_asignada > self.demanda_facturada):
                demanda_equivalente = self.demanda_asignada
            else:
                demanda_equivalente = self.demanda_facturada
            linea_consumo = self.linea_electricidad.search([['clasificacion','=','demanda']])
            tarifa = ( self.monto_total_demanda / self.dias_lectura) * (30 / demanda_equivalente)
            linea_consumo.write(
                {
                    'cantidad': demanda_equivalente,
                    'precio_unidad':tarifa,
                    'subtotal': demanda_equivalente * tarifa
                }
            )
            self._onchange_subtotal()

    @api.onchange('linea_electricidad')
    def _onchange_subtotal(self):
        for record in self:
            if record.linea_electricidad is not None:
                record.subtotal_electricidad = 0
                for line in record.linea_electricidad:
                    record.subtotal_electricidad += line["subtotal"]

                for invoice_line in record.invoice_line_ids:
                    if invoice_line.product_id.clasificacion == 'electricidad':
                        invoice_line.write( {
                            'price_unit': record.subtotal_electricidad
                        })
                        invoice_line._onchange_price_subtotal()
