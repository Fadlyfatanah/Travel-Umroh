from odoo import models, fields, api

class ScheduleLine(models.Model):
    _name = 'schedule.line'
    _description = 'Schedule Line'
    
    name = fields.Char(required=True, size=40)
    date = fields.Date(required=True, size=8)
    travel_id = fields.Many2one('travel.package')
