from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    package_id = fields.Many2one('travel.package', string='Travel Packages', domain=[('state', '=', 'confirm')])
    manifest_line = fields.One2many('manifest.lines', 'order_id')

    @api.onchange('package_id')
    def button_update(self):
        for rec in self:
            product = rec.package_id.product_id
            order_list = [(5, 0, 0)]
            order_list.append([0, 0, {
                'product_id': product.id,
                'name': product.description,
                'product_uom_qty': 1,
                'price_unit': product.list_price,
                'tax_id': product.taxes_id,
                'price_subtotal': product.list_price * 1,
                'product_uom': 1
            }])
            rec.order_line = order_list