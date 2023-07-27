from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'
    
    package_ok = fields.Boolean('Travel Package')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _set_standard_price(self, products):
        for product in products:
            standard_price = product.product_template_attribute_value_ids\
                .mapped('product_attribute_value_id').mapped('package_id').mapped('subtotal')
            product.standard_price = sum(standard_price)
    
    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self).create(vals_list)
        self._set_standard_price(products)
        return products
    
class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    
    package_id = fields.Many2one('travel.package', string='Package')