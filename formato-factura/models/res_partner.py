# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PartnerCodeInherit( models.Model):
    _inherit = 'res.partner'
    country_id = fields.Many2one(string='pais', comodel_name='res,country', default=238)
    partner_code = fields.Char(string = 'Código de Interlocutor', default=lambda self: self._get_next_sequence_number() )
    titular = fields.Char(string = 'titular de pago')
    dir_fisc = fields.Text(string = 'Direccion fiscal')
    contract_accounts = fields.One2many(string = 'Cuentas contrato', comodel_name = 'contract.accounts', inverse_name = 'titular')
    
    @api.model
    def create(self, vals):
        vals['partner_code'] = self.env['ir.sequence'].next_by_code('partner_code_seq')
        result = super( PartnerCodeInherit, self).create(vals)
        return result 

    @api.model
    def _get_next_sequence_number(self):
        for record in self:
            sequence = self.env['ir.sequence'].search([('code','=','partner_code_seq')])
            next= sequence.get_next_char(sequence.number_next_actual)
            return next