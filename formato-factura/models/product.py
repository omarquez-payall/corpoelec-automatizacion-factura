# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Product( models.Model):
    _inherit = 'product.template'

    #------------------- Campo para identificar productos precargados en factura electricidad ------------------

    
    precargar = fields.Boolean( string = "Precargar", default = False)
    clasificacion = fields.Selection(
        string="Clasificacion de la linea",
        selection=[
            ('electricidad','Electricidad'),
            ('aseo', 'Aseo'),
            ('relleno', 'relleno'),
            ('otro', 'Otro cargo')
        ],
        default = 'otro'
    )
    