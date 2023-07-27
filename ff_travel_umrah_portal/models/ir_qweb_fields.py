from odoo import models, api, _
from odoo.tools import html_escape as escape

class Contact(models.AbstractModel):
    _inherit = 'ir.qweb.field.contact'

    @api.model
    def value_to_html(self, value, options):
        if not value:
            return ''

        opf = options and options.get('fields') or ["name", "address", "phone", "mobile", "email"]
        opsep = options and options.get('separator') or "\n"
        value = value.sudo().with_context(show_address=True)
        name_get = value.name_get()[0][1]

        val = {
            'name': name_get.split("\n")[0],
            'address': escape(opsep.join(name_get.split("\n")[1:])).strip(),
            'phone': value.phone,
            'mobile': value.mobile,
            'city': value.city,
            'country_id': value.country_id.display_name,
            'website': value.website,
            'email': value.email,
            'vat': value.vat,
            'vat_label': value.country_id.vat_label or _('VAT'),
            'ktp_no': value.ktp_no,
            'fields': opf,
            'object': value,
            'options': options
        }
        return self.env['ir.qweb']._render('base.contact', val, **options.get('template_options', dict()))
