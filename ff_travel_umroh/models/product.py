from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'
    
    package_ids = fields.One2many('travel.package', 'product_id', 'Packages', domain=[('state', '=', 'open')])
    package_ok = fields.Boolean('Travel Package')
