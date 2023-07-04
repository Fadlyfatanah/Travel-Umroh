# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    contact_name_payment_info = fields.Char(string="Contact name for payment information")
    contact_media_payment_info = fields.Char(string="Media to use for payment information")
    contact_payment_info = fields.Char(string="Contact for payment information")
