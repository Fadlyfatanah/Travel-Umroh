# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ManifestLinesTravel(models.Model):
    _name = 'manifest.lines.travel'
    _description = 'Manifest Lines Travel'
    
    name = fields.Many2one('manifest.lines')
    ktp_no = fields.Char(related='name.ktp_no')
    date_birth = fields.Date(related='name.date_birth')
    place_birth = fields.Char(related='name.place_birth')
    pass_no = fields.Char(related='name.pass_no')
    date_exp = fields.Date(related='name.date_exp')
    pass_name = fields.Char(related='name.pass_name')
    date_isue = fields.Date(related='name.date_isue')
    imigrasi = fields.Char(related='name.imigrasi')
    gender = fields.Selection(related='name.gender')
    room_type = fields.Selection(related='name.room_type')
    age = fields.Integer(related='name.age')
    travel_id = fields.Many2one('travel.package', string='Travel')
    mahram = fields.Many2one(related='name.mahram')
    agent = fields.Many2one('res.users')
    # order_id = fields.Many2one('sale.order', string='Sale')

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
    pass_img = fields.Binary(related='name.pass_img')
    ktp_img = fields.Binary(related='name.ktp_img')
    doc_img = fields.Binary(related='name.doc_img')
    kk_img = fields.Binary(related='name.kk_img')
    title = fields.Selection(related='name.title')
    gender = fields.Selection(related='name.gender')
    partner_id = fields.Many2one('res.partner', string='Partner')
    travel_id = fields.Many2one('travel.package', string='Travel')
    age = fields.Integer()
    mahram = fields.Many2one('res.partner', string='Mahram', attrs={'invisible': [('id', '=', 'name.id')]})
    notes = fields.Char(string='Notes')
    order_id = fields.Many2one('sale.order', string='Sale')
    room_type = fields.Selection([
        ('del', 'Deluxe'),
        ('tri', 'Triple'),
        ('quad', 'Quad'),
        ('reg', 'Regular')
    ])
    
    @api.onchange('date_birth')
    def _compute_calculate_age(self):
        for rec in self:
            if rec.date_birth:
                today = rec.date_birth.today()
                born = rec.date_birth
                rec.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))


        
