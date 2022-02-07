# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InvoiceImagesInherit( models.Model):
    _inherit = 'account.move'
    images = fields.Many2one( string = 'Imágenes para facturas', comodel_name = 'invoices.images', default=1)