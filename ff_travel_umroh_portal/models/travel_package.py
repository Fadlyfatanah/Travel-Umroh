from odoo import models, fields, api

class TravelPackage(models.Model):
    _inherit = 'travel.package'
    _description = 'Travel Package'
    
    def _compute_access_url(self):
        super(TravelPackage, self)._compute_access_url()
        for package in self:
            package.access_url = '/my/package/%s' % package.id