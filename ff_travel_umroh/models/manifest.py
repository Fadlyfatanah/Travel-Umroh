# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ManifestLines(models.Model):
    _name = 'manifest.lines'
    _description = 'Manifest Lines'

    name = fields.Many2one('res.partner', string='Jamaah', required=True)
    ktp_no = fields.Char(related='name.ktp_no')
    date_birth = fields.Date(related='name.date_birth')
    place_birth = fields.Char(related='name.place_birth')
    pass_no = fields.Char(related='name.pass_no')
    date_exp = fields.Date(related='name.date_exp')
    pass_name = fields.Char(related='name.pass_name')
    date_isue = fields.Date(related='name.date_isue')
    imigrasi = fields.Char(related='name.imigrasi')
    title = fields.Many2one(related='name.title', ondelete='cascade')
    gender = fields.Selection(related='name.gender')
    partner_id = fields.Many2one('res.partner', string='Partner')
    travel_id = fields.Many2one('travel.package')
    age = fields.Integer()
    mahram = fields.Many2one('res.partner', string='Mahram')
    notes = fields.Char(string='Notes')
    order_id = fields.Many2one('sale.order', string='Sale')
    agent = fields.Many2one('res.users')
    room_type = fields.Selection([
        ('del', 'Deluxe'),
        ('tri', 'Triple'),
        ('quad', 'Quad'),
        ('reg', 'Regular')
    ])

    def calculate_age(self):
        if self.date_birth:
            today = self.date_birth.today()
            born = self.date_birth
            self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    @api.onchange('date_birth')
    def _onchange_calculate_age(self):
        self.calculate_age()

    @api.depends('date_birth')
    def _compute_calculate_age(self):
        for rec in self:
            rec.calculate_age()

    @api.onchange('name')
    def _onchange_domain(self):
        domain = {'domain': {}}
        jamaah_ids = self.env['res.partner'].search([]).filtered(lambda x:\
            x.jamaah == True and x.id != self.name.id)
        if self.name:
            domain['domain']['mahram'] = [('id', 'in', jamaah_ids.ids)]
        else:
            domain['domain']['name'] = [('id', 'in', jamaah_ids.ids)]

        return domain