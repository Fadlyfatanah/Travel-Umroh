from odoo import models, fields

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    
    package_id = fields.Many2one('travel.package', string='Package')