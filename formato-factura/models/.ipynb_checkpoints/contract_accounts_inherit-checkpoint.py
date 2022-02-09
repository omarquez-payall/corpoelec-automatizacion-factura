# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContractAccountsInherit( models.Model):
    _inherit = 'account.move'
    
    contract_accounts = fields.Many2one(string = 'Cuentas contrato', comodel_name = 'contract.accounts')