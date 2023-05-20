from odoo import models, fields

class ResClothesSize(models.Model):
    _name = 'res.clothes.size'
    _description = 'Res Clothes Size'
    
    name = fields.Char('Name')