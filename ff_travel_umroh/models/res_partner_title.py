from odoo import models, fields

class ResPartnerTitle(models.Model):
    _inherit = 'res.partner.title'
    _description = 'Res Partner Title'
    
    type = fields.Selection([
        ('person', 'Individual'),
        ('company', 'Company')
    ], string='Type')