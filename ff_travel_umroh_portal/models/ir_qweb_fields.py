from odoo import models, fields, api, _
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

    # @api.model
    # def get_available_options(self):
    #     options = super(Contact, self).get_available_options()
        # contact_fields = [
        #     {'field_name': 'name', 'label': _('Name'), 'default': True},
        #     {'field_name': 'address', 'label': _('Address'), 'default': True},
        #     {'field_name': 'phone', 'label': _('Phone'), 'default': True},
        #     {'field_name': 'mobile', 'label': _('Mobile'), 'default': True},
        #     {'field_name': 'email', 'label': _('Email'), 'default': True},
        #     {'field_name': 'vat', 'label': _('VAT')},
        #     {'field_name': 'ktp_no', 'label': _('KTP'), 'default': True},
        # ]
        # separator_params = dict(
        #     type='selection',
        #     selection=[[" ", _("Space")], [",", _("Comma")], ["-", _("Dash")], ["|", _("Vertical bar")], ["/", _("Slash")]],
        #     placeholder=_('Linebreak'),
        # )
        # options.update(
        #     fields=dict(type='array', params=dict(type='selection', params=contact_fields), string=_('Displayed fields'), description=_('List of contact fields to display in the widget'), default_value=[param.get('field_name') for param in contact_fields if param.get('default')]),
        #     separator=dict(type='selection', params=separator_params, string=_('Address separator'), description=_('Separator use to split the address from the display_name.'), default_value=False),
        #     no_marker=dict(type='boolean', string=_('Hide badges'), description=_("Don't display the font awesome marker")),
        #     no_tag_br=dict(type='boolean', string=_('Use comma'), description=_("Use comma instead of the <br> tag to display the address")),
        #     phone_icons=dict(type='boolean', string=_('Display phone icons'), description=_("Display the phone icons even if no_marker is True")),
        #     country_image=dict(type='boolean', string=_('Display country image'), description=_("Display the country image if the field is present on the record")),
        # )
        # return options