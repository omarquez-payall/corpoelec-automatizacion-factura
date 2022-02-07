# -*- coding: utf-8 -*-
{
    'name': "formato-factura",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

    # always loaded
    'data': [
        'security/invoices_images_security.xml',
        'security/ir.model.access.csv',
        'data/invoices_images.xml',
        'views/invoice_images.xml',
        'views/invoice_images_inherit.xml',
        'views/res_partner_inherit.xml',
        'views/contract_accounts.xml',
        'report/external_layout_background_inherit.xml',
        'report/report_invoice_document.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
