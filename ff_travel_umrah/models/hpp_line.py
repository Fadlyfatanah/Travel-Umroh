from odoo import models, fields, api

class HppLines(models.Model):
    _name = 'hpp.line'
    _description = 'Hpp Line'
    
    name = fields.Char('Product', size=25)
    product_qty = fields.Float(string='Quantity', default=1, size=3)
    travel_id = fields.Many2one('travel.package', string='Travel')
    product_uom = fields.Many2one('uom.uom', string='UoM')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', size=12)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, size=14)

    @api.depends('product_qty', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.product_qty * rec.price