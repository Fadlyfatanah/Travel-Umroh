from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    airlines = fields.Boolean(string='Airlines ?')
    hotel = fields.Boolean(string='Hotel ?')
    jamaah = fields.Boolean(string='Jamaah ?')
    muthawif = fields.Boolean(string='Muthawif ?')
    ktp_no = fields.Char(string='KTP No', size=16)
    father_name = fields.Char(string='Father\'s Name', size=25)
    job = fields.Char(string='Job', size=25)
    date_birth = fields.Date(string='Date of Birth', size=8)
    mother_name = fields.Char(string='Mother\'s Name', size=25)
    place_birth = fields.Char(string='Place of Birth', size=25)
    pass_no = fields.Char(string='Passport No')
    date_exp = fields.Date(string='Date of Expiry', size=8)
    pass_name = fields.Char(string='Passport Name')
    date_isue = fields.Date(string='Date Issued', size=8)
    imigrasi = fields.Char(string='Imigrasi', size=25)
    pass_img = fields.Binary(string='Passport')
    ktp_img = fields.Binary(string='KTP')
    doc_img = fields.Binary(string='Buku Nikah / Akta Lahir')
    kk_img = fields.Binary(string='Kartu Keluarga')
    country_id = fields.Many2one('res.country', string='Country')
    clothes_size_id = fields.Many2one('res.clothes.size', string='Clothes Size')
    marital_status_id = fields.Many2one('res.marital.status', string='Marital Status')
    education_id = fields.Many2one('res.education', string='Education')
    title_id = fields.Many2one('res.partner.title', string='Title')
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

    @api.depends('is_company', 'name', 'parent_id.display_name', 'type', 'company_name', 'commercial_company_name')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None, html_format=None, show_vat=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)
