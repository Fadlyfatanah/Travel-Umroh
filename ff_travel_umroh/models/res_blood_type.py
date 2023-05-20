from odoo import models, fields

class ResBloodType(models.Model):
    _name = 'res.blood.type'
    _description = 'Res Blood Type'
    
    name = fields.Char('Name')