from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    airlines = fields.Boolean(string='Airlines ?')
    hotel = fields.Boolean(string='Hotel ?')
    jamaah = fields.Boolean(string='Jamaah ?')
    muthawif = fields.Boolean(string='Muthawif ?')
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
    country_id = fields.Many2one('res.country', string='Country')
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