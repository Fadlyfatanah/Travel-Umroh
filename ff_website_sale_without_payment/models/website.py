# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    website_sale_payment = fields.Boolean(string='E-Commerce With Payments')
