from odoo import models, fields, api
from datetime import timedelta

class HotelLines(models.Model):
    _name = 'hotel.lines'
    _description = 'Hotel Lines'

    name = fields.Many2one('res.partner', 'Hotel', required=True, domain=[('hotel', '=', True)])  
    start_date = fields.Date(required=True, )
    end_date = fields.Date(required=True, )
    city = fields.Char(related='name.city', readonly=True)
    travel_id = fields.Many2one('travel.package', string='Travel')

class AirlineLines(models.Model):
    _name = 'airline.lines'
    _description = 'Airline Lines'
    
    name = fields.Many2one('res.partner', string='Airlines', required=True, domain=[('airlines', '=', True)])
    departure_date = fields.Date(required=True, )
    departure_city = fields.Char(required=True, )
    arrival_city = fields.Char(required=True, )
    travel_id = fields.Many2one('travel.package', string='Travel')

class ScheduleLines(models.Model):
    _name = 'schedule.lines'
    _description = 'Schedule Lines'
    
    name = fields.Char(required=True)
    date = fields.Date(required=True, )
    travel_id = fields.Many2one('travel.package', string='Travel')

class HppLines(models.Model):
    _name = 'hpp.lines'
    _description = 'Hpp Lines'
    
    name = fields.Many2one('product.product', 'Product')
    product_qty = fields.Float(string='Quantity')
    travel_id = fields.Many2one('travel.package', string='Travel')
    product_uom = fields.Many2one('uom.uom', string='UoM')
    price = fields.Float(string='Unit Price', digits=(6, 2))
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_get_price', store=True,)

    @api.depends('product_qty', 'price')
    def _compute_get_price(self):
        for rec in self:
            rec.price_subtotal = rec.product_qty * rec.price

