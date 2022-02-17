# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCountryInherit( models.Model):
    _inherit = 'res.country.state'
    
    short_code = fields.Char(string = 'Codigo corto')