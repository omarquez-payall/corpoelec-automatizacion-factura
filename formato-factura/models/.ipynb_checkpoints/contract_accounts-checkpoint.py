# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContractAccounts( models.Model):
    _name = 'contract.accounts'
    _description = 'This model is to load Corpoelect customers contract accounts'
    
    cod = fields.Char(string = 'Codigo de cta')
    no_cta_contrato = fields.Char(string = 'Cuenta Contrato')
    cnae = fields.Char(string = 'CNAE')
    medidor = fields.Char(string = 'Identificador de Medidor')
    address_suministro = fields.Text(string = 'Dirección de Suministro')
    titular = fields.Many2one(string = 'Titular', comodel_name = 'res.partner')
    tarifa = fields.Float(string = 'Demanda asignada')
    fecha_creacion = fields.Date(string = 'Fecha de creación')
    
    @api.model
    def create(self, vals):
        vals['cod'] = self.env['ir.sequence'].next_by_code('con_accounts_seq')
        result = super( ContractAccounts, self).create(vals)
        return result 

    @api.model
    def _get_next_sequence_number(self):
        for record in self:
            sequence = self.env['ir.sequence'].search([('code','=','con_accounts_seq')])
            next= sequence.get_next_char(sequence.number_next_actual)
            return next