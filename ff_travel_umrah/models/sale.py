from odoo import models, fields, _
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    manifest_line = fields.One2many('manifest.lines', 'order_id')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Sale Order Line'
    
    state = fields.Selection(related='order_id.state')
    