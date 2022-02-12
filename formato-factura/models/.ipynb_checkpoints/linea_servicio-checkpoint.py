# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LineaServicio( models.Model):
    _name = 'linea.servicio'
    _description = 'Modelo para la linea de los servicios'

    move_id = fields.Many2one( comodel_name = "account.move", string = "Linea de Energia")
    move_aseo_id = fields.Many2one( comodel_name = "account.move", string = "Linea de Aseo")
    move_relleno_id = fields.Many2one( comodel_name = "account.move", string = "Linea de Relleno")
    nombre_cargo = fields.Char( string = "Cargo", store = True)
    tipo = fields.Selection(
        string="Tipo",
        selection=[
            ('principal','Principal'),
            ('otro', 'Otro cargo'),
            ('aseo', 'Aseo'),
            ('relleno', 'relleno')
        ],
        default = 'otro', store = True
    )
    clasificacion = fields.Selection(
        string="Clasificacion de la linea",
        selection=[
            ('consumo','Consumo'),
            ('demanda', 'Demanda'),
            ('combustible','Combustible'),
            ('otro', 'Otro cargo'),
            ('aseo', 'Aseo'),
            ('relleno', 'relleno')
        ],
        default = 'otro'
    )
    cantidad = fields.Integer( string = "Cantidad", store = True)
    precio_unidad = fields.Float( string = "Precio", store = True)
    subtotal = fields.Float( string = "Subtotal", readonly=True, store = True)

    @api.onchange('precio_unidad','cantidad')
    def _onchange_subtotal(self):
        self.subtotal = self.cantidad * self.precio_unidad

    @api.model
    def write(self,vals):
        rec = super(LineaServicio, self).write(vals)
        return rec