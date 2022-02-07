# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class Aseo( models.Model):
    _inherit = 'account.move'
    #_name = "servicio.electricidad"
    #_description = "Modelo creado para el detalle del servicio de electricidad"

    #-------------- FACTURA ---------------------------------------
    #lineas_detalle = fields.
    #factura_id = fields.Many2one(
    #    comodel_name = "account.move"
    #)
    #dias_lectura = fields.Integer( string ="Dias Lectura", related ="factura_id.dias_lectura")
    """ linea_servicio_aseo = fields.One2many(
        comodel_name="linea.servicio", 
        inverse_name="move_aseo_id",
        
        states={'draft': [('readonly', False)]}) """
    
    cuenta_contrato = fields.Many2one( 
        string="No Cuenta Contrato",
        comodel_name = "contract.accounts"
    )
    subtotal_aseo = fields.Float( string="Subtotal Aseo", store=True)
    #-------------- SECCION DE CONSUMO ---------------------------