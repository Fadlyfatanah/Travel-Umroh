# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class Partner(models.Model):
    _inherit = 'res.partner'

    airlines = fields.Boolean(string='Airlines ?')
    hotel = fields.Boolean(string='Hotel ?')
    ktp_no = fields.Char(string='KTP No')
    father_name = fields.Char(string='Father\'s Name')
    job = fields.Char(string='Job')
    date_birth = fields.Date(string='Date of Birth')
    mother_name = fields.Char(string='Mother\'s Name')
    place_birth = fields.Char(string='Place of Birth')
    pass_no = fields.Char(string='Passport No')
    date_exp = fields.Date(string='Date of Expiry')
    pass_name = fields.Char(string='Passport Name')
    date_isue = fields.Date(string='Date Issued')
    imigrasi = fields.Char(string='Imigrasi')
    pass_img = fields.Binary(string='Passport')
    ktp_img = fields.Binary(string='KTP')
    doc_img = fields.Binary(string='Buku Nikah / Akta Lahir')
    kk_img = fields.Binary(string='Kartu Keluarga')
    title = fields.Selection([
        ('mr', 'Mister'),
        ('miss', 'Miss'),
        ('doctor', 'Doctor'),
        ('madam', 'Madam'),
        ('prof', 'Professor')
    ], string='Title')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorce', 'Divorce')
    ], string='Marital Status')
    gender = fields.Selection([
        ('man', 'Man'),
        ('woman', 'Woman')
    ], string='Gender')
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string='Blood Type')
    education = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('diploma', 'DIPLOMA'),
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
    ], string='Education')
    clothes_size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('4l', '4L'),
    ], string='Clothes Size')

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

    class SaleOrder(models.Model):
        _inherit = 'sale.order'
        _description = 'Sale Order'

        package_id = fields.Many2one('travel.package', string='Travel Packages', domain=[('state', '=', 'confirm')])
        manifest_line = fields.One2many('manifest.lines', 'order_id')

        @api.onchange('package_id')
        def button_update(self):
            for rec in self:
                product = rec.package_id.product_id
                order_list = [(5, 0, 0)]
                order_list.append([0, 0, {
                    'product_id': product.id,
                    'name': product.description,
                    'product_uom_qty': 1,
                    'price_unit': product.list_price,
                    'tax_id': product.taxes_id,
                    'price_subtotal': product.list_price * 1,
                    'product_uom': 1
                }])
                rec.order_line = order_list
        
