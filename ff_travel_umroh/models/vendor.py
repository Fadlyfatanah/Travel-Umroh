from odoo import models, fields, api
from datetime import timedelta

class HotelLines(models.Model):
    _name = 'hotel.lines'
    _description = 'Hotel Lines'

    name = fields.Many2one('res.partner', 'Hotel', required=True, domain=[('hotel', '=', True)])  
    start_date = fields.Date(required=True, )
    end_date = fields.Date(required=True, )
    city = fields.Char(related='name.city', readonly=True)
    travel_id = fields.Many2one('travel.package')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', tracking=True)

class AirlineLines(models.Model):
    _name = 'airline.lines'
    _description = 'Airline Lines'
    
    name = fields.Many2one('res.partner', string='Airline', required=True, domain=[('airlines', '=', True)])
    departure_date = fields.Date(required=True, )
    departure_city = fields.Char(required=True, )
    arrival_city = fields.Char(required=True, )
    travel_id = fields.Many2one('travel.package')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', tracking=True)

class EquipmentLine(models.Model):
    _name = 'equipment.lines'
    _description = 'Equipment Line'
    _rec_name = 'product_id'
    
    product_id = fields.Many2one('product.product', string='Product', domain="[('package_ok', '=', False)]")
    travel_id = fields.Many2one('travel.package')
    product_qty = fields.Integer('Quantity', default=1)
    product_uom = fields.Many2one('uom.uom', string='UoM')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', tracking=True)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, tracking=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.price = self.product_id.list_price
        self.product_uom = self.product_id.uom_id

    @api.depends('product_qty', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.product_qty * rec.price

class ScheduleLines(models.Model):
    _name = 'schedule.lines'
    _description = 'Schedule Lines'
    
    name = fields.Char(required=True)
    date = fields.Date(required=True, )
    travel_id = fields.Many2one('travel.package')

class HppLines(models.Model):
    _name = 'hpp.lines'
    _description = 'Hpp Lines'
    
    name = fields.Char('Product')
    product_qty = fields.Float(string='Quantity', default=1)
    travel_id = fields.Many2one('travel.package', string='Travel')
    product_uom = fields.Many2one('uom.uom', string='UoM')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', tracking=True)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, tracking=True)

    @api.depends('product_qty', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.product_qty * rec.price