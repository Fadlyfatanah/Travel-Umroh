from odoo import models, fields, api

class HotelLine(models.Model):
    _name = 'hotel.line'
    _description = 'Hotel Line'

    name = fields.Many2one('res.partner', 'Hotel', required=True, domain=[('hotel', '=', True)])  
    start_date = fields.Date(required=True, size=8)
    end_date = fields.Date(required=True, size=8)
    city = fields.Char(related='name.city', readonly=True)
    travel_id = fields.Many2one('travel.package')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', size=14)
