# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IntegacionPayall( models.Model):
    _name ='integracion.payall'
    _description = 'Modelo para la integracion con Payall a traves de la API'


    def consultaDeudaCliente():
        
        return None
    
    @api.model
    def pagarDeduaCliente(self):
        invoices = self.env['account.move'].search([['partner_id.id','=',41], ['move_type','=','out_invoice']])
        payment_method = self.env['account.payment.method'].search([['code','=','manual'],['payment_type','=','inbound']])
        active_ids = invoices.ids
        payments = self.env['account.payment.register'].with_context(active_model='account.move', active_ids=active_ids).create({
            'amount': 30000.00,
            'group_payment': True,
            'payment_difference_handling': 'open',
            'currency_id': self.env.company['currency_id'].id,
            'payment_method_id': payment_method.id,
        })._create_payments()
        return True