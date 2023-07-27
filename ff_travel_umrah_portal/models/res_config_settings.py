# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contact_name_payment_info = fields.Char(
        related="website_id.contact_name_payment_info",
        readonly=False,
    )
    contact_media_payment_info = fields.Char(
        related="website_id.contact_media_payment_info",
        readonly=False,
    )
    contact_payment_info = fields.Char(
        related="website_id.contact_payment_info",
        readonly=False,
    )
