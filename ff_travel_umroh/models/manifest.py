# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ManifestLinesTravel(models.Model):
    _name = 'manifest.lines.travel'
    _description = 'Manifest Lines Travel'
    _rec_name = 'pass_name'
    
    pass_name = fields.Char(string='Passport Name')
    age = fields.Integer('Age')
    travel_id = fields.Many2one('travel.package', string='Travel')
    mahram = fields.Many2one('res.partner', string='Mahram')
    agent = fields.Many2one('res.users')
    ktp_no = fields.Char(string='KTP No')
    date_birth = fields.Date(string='Date of Birth')
    place_birth = fields.Char(string='Place of Birth')
    pass_no = fields.Char(string='Passport No')
    date_exp = fields.Date(string='Date of Expiry')
    date_isue = fields.Date(string='Date Issued')
    imigrasi = fields.Char(string='Imigrasi')
    room_type = fields.Selection([
        ('del', 'Deluxe'),
        ('tri', 'Triple'),
        ('quad', 'Quad'),
        ('reg', 'Regular')
    ], string='Room Type')
    gender = fields.Selection([
        ('man', 'Man'),
        ('woman', 'Woman')
    ], string='Gender')

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


        
