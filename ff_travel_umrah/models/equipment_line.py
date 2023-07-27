from odoo import models, fields, api

class EquipmentLine(models.Model):
    _name = 'equipment.line'
    _description = 'Equipment Line'
    _rec_name = 'product_id'
    
    product_id = fields.Many2one('product.product', string='Product', domain="[('package_ok', '=', False)]")
    travel_id = fields.Many2one('travel.package')
    product_qty = fields.Integer('Quantity', default=1, size=3)
    product_uom = fields.Many2one('uom.uom', string='UoM')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', size=12)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, size=14)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.price = self.product_id.list_price
        self.product_uom = self.product_id.uom_id

    @api.depends('product_qty', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.product_qty * rec.price
