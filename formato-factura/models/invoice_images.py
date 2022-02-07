# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InvoiceImages( models.Model):
    _name = 'invoices.images'
    _description = 'This model is to load and manage the images needed for the invoice template'
    logo = fields.Binary(string='Logo')
    header_logo = fields.Binary(string='Header Logo')
    full_logo = fields.Binary(string='Full Logo')
    payment_methods = fields.Binary(string='Payment Methods')
    advertisement = fields.Binary(string='Publicidad de corpoelect bajo imagen de los metodos de pago')
    service_icon_1 = fields.Binary(string='Icono de servicio 1')
    service_icon_2 = fields.Binary(string='Icono de servicio 2')
    service_icon_3 = fields.Binary(string='Icono de servicio 3')
    footer_icon_1 = fields.Binary(string='Icono de pie de pagina 1')
    footer_icon_2 = fields.Binary(string='Icono de pie de pagina 2')
    footer_icon_3 = fields.Binary(string='Icono de pie de pagina 3')
    