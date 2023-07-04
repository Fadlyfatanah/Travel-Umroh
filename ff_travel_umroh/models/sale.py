from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    manifest_line = fields.One2many('manifest.lines', 'order_id')

    def action_confirm(self):
        # msg = self.quantity_check()
        msg=''
        if msg != '':
            raise UserError(msg)
        super(SaleOrder, self).action_confirm()

    def quantity_check(self):
        msg = ''
        for line in self.order_line:
            if line.product_id.package_ok:
                qty = line.product_uom_qty
                manifest_count = len(self.manifest_line\
                    .filtered(lambda o: o.travel_id == line.package_id))

                if manifest_count > qty:
                    msg += 'Quantity of Jamaah more than quantity of travel package (%s) \n' %line.product.name
        return msg

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Order Line'
    
    state = fields.Selection(related='order_id.state')
    