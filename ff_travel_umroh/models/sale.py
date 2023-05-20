from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    manifest_line = fields.One2many('manifest.lines', 'order_id')
    package_id = fields.Many2one('travel.package', string='Travel Package')

    @api.onchange('package_id')
    def _onchange_package_id(self):
        for rec in self:
            product = rec.package_id.product_id
            if product:
                order_list = [(5, 0, 0)]
                order_list.append((0, 0, {
                    'product_id': product.id,
                    'name': product.description,
                    'product_uom_qty': 1,
                    'price_unit': product.list_price,
                    'tax_id': product.taxes_id.ids,
                    'price_subtotal': product.list_price * 1,
                    'product_uom': 1
                }))
                rec.order_line = order_list
    
    def action_confirm(self):
        product_id = self.package_id.product_id
        line_target_id = self.order_line.filtered(lambda o: o.product_id.id == product_id.id)
        len_manifest_line = len(self.manifest_line)
        if line_target_id[0].product_uom_qty != len_manifest_line:
            raise UserError('Manifest line (Jamaah) more than quantity of travel package')
        super(SaleOrder, self).action_confirm()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Order Line'
    
    state = fields.Selection(related='order_id.state')
    # package_id = fields.Many2one('travel.package', related='product_id.package_id')
    