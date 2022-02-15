# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime


class AccountMove( models.Model):
    _inherit = 'account.move'

    #------------------- Relacion con los servicios ------------------
    No_Contable = fields.Char( string = 'No Doc Contable',readonly=True, required = True, index=True, default=lambda self: self._get_next_sequence_number_contable())
    No_Registro = fields.Char( string = 'No Registro',readonly=True, required = True, index=True, default=lambda self: self._get_next_sequence_number_registro())
    
    cuenta_contrato = fields.One2many( 
        string="No Cuenta Contrato",
        comodel_name = "contract.accounts",
        store=True,
        inverse_name = "move_id"
    )
    
    inicio_periodo = fields.Date(string='Inicio período', default=fields.Date.today, store=True)
    fin_periodo = fields.Date(string='Fin período', default=fields.Date.today, store=True)
    #------------ Servicio Electrividad ------------------------
    #electricidad_detalle = fields.One2many(
    #    comodel_name = "servicio.electricidad", 
    #    inverse_name = "factura_id")

    dias_lectura = fields.Integer( string = "Dias Lectura", store = True)
    cargar_productos = fields.Boolean( string="Cargar", default = False)
    saldo_vencido = fields.Float( string="Saldo Vencido", default = 0.0)
    # COMO DEBE ESTAR EN PRODUCCION
    #dias_lectura = fields.Integer( string = "Dias Lectura", required = True)
    #CREAR LINEAS DEL SERVICIO DE ELECTRICIDAD, ASEO Y RELLENO
    
    @api.onchange('inicio_periodo')
    def expiration_date(self):
        for record in self:
            record.dias_lectura = record.inicio_periodo.day
            
            

    @api.model
    def create(self, vals):
        vals['No_Contable'] = self.env['ir.sequence'].next_by_code('Seq_No_Contable')
        vals['No_Registro'] = self.env['ir.sequence'].next_by_code('Seq_No_Registro')
        vals['No_Registro'] = self.env['ir.sequence'].next_by_code('seq_fact')
        result = super(AccountMove, self).create(vals)
        return result 

    @api.model
    def _get_next_seq_fact(self):
        sequence = self.env['ir.sequence'].search([('code','=', 'seq_fact')])
        edo = self.env['res.country.state'].search([('id','=',self.state_id)])
        next = sequence.get_next_char(sequence.number_next_actual)
        self.name = 'SERIECC' + edo.short_code + '163' + next
    
    @api.model
    def _get_next_sequence_number_contable(self):
        sequence = self.env['ir.sequence'].search([('code','=', 'Seq_No_Contable')])
        next = sequence.get_next_char(sequence.number_next_actual)
        return next

    @api.model
    def _get_next_sequence_number_registro(self):
        sequence = self.env['ir.sequence'].search([('code','=', 'Seq_No_Registro')])
        next = sequence.get_next_char(sequence.number_next_actual)
        return next

    @api.onchange('partner_id')
    def _filtrar_cuentas_contrato(self):
        for record in self:
            if record.partner_id:
                return { 'domain': { 'cuenta_contrato': [('titular.id','=',record.partner_id.id)]}}

    def cargar_productos_electricidad(self):
        for record in self:
            products = self.env['product.product'].search( [['precargar','=',True]])
            
            for product in products:
                #CAMBIAR ACCOUNT_ID CUANDO SE SEPA A CUAL VA
                record.invoice_line_ids.create({
                    'name': product.name,
                    'price_unit': product.price,
                    'quantity': 1,
                    'product_id': product.id,
                    'account_id': 1,
                    'move_id': record.id
                })
                record.cargar_productos = True
            record.linea_electricidad.create({
                'move_id': record.id,
                'nombre_cargo': 'FACTURACION POR CONSUMO',
                'cantidad': 1,
                'tipo':'principal',
                'clasificacion':'consumo',
                'precio_unidad':1,
                'subtotal':1
            })
            record.linea_electricidad.create({
                'move_id': record.id,
                'nombre_cargo': 'CARGO POR AJUSTE COMBUSTIBLE Y ENERGIA',
                'cantidad': 1,
                'tipo':'otro',
                'clasificacion':'combustible',
                'precio_unidad':1,
                'subtotal':1
            })
            record.linea_electricidad.create({
                'move_id': record.id,
                'nombre_cargo': 'FACTURACION POR DEMANDA',
                'cantidad': 1,
                'tipo':'principal',
                'clasificacion':'demanda',
                'precio_unidad':1,
                'subtotal':1
            })