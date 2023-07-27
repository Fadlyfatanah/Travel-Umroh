from odoo import models, fields

class ResMaritalStatus(models.Model):
    _name = 'res.marital.status'
    _description = 'Res Marital Status'
    
    name = fields.Char('Name', size=10)