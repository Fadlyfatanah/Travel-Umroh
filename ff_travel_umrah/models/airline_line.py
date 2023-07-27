from odoo import models, fields, api

class AirlineLines(models.Model):
    _name = 'airline.line'
    _description = 'Airline Line'
    
    name = fields.Many2one('res.partner', string='Airline', required=True, domain=[('airlines', '=', True)])
    departure_date = fields.Date(required=True, size=8)
    departure_city = fields.Char(required=True, size=25)
    arrival_city = fields.Char(required=True, size=25)
    travel_id = fields.Many2one('travel.package')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')
    price = fields.Monetary(string='Price', size=14)
