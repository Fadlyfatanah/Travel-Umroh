from odoo import models, fields

class ResEducation(models.Model):
    _name = 'res.education'
    _description = 'Res Education'
    
    name = fields.Char('Name', size=10)