# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta


class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Travel Package'
    _inherit = 'mail.thread'

    name = fields.Char(required=True, copy=False, readonly=True, index=True, default=lambda self: _('/'))
    departure_date = fields.Date(required=True, )
    return_date = fields.Date(required=True, )
    product_id = fields.Many2one('product.product', 'Sale', required=True, )
    package_id = fields.Many2one('mrp.bom', 'Package', required=True, )
    quota = fields.Integer()
    hotel_line = fields.One2many('hotel.lines', 'travel_id')
    airlines_line = fields.One2many('airline.lines', 'travel_id', string='Airlines')
    schedule_line = fields.One2many('schedule.lines', 'travel_id', string='Schedule')
    hpp_line = fields.One2many('hpp.lines', 'travel_id')
    remaining_seats = fields.Integer(compute='_get_manifest_count', readonly=True)
    quota_progress = fields.Float(compute='_compute_quota_progress')
    manifest_travel_line = fields.One2many('manifest.lines.travel', 'travel_id', readonly=True)
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, track_visibility='always', track_sequence=6, compute='_compute_get_price_total')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', readonly=True, states={
                                   'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Pricelist for current sales order.")
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done')
    ], default='draft')

    @api.depends('quota', 'manifest_travel_line')
    def _compute_quota_progress(self):
        for r in self:
            if len(r.manifest_travel_line) <= r.quota and r.quota > 0:
                r.quota_progress = 100.0 * (len(r.manifest_travel_line) / r.quota)
            # else:
            #     return {
            #         'value': {
            #                   'quota_progress': 0 # mengisi field seats dengan nilai jumlah peserta atau 1
            #                 #   'manifest_line': 0
            #                   },
            #         'warning': {
            #                     'title': "Jumlah Peserta Tidak Valid", # judul pop up
            #                     'message': "Jumlah peserta tidak boleh lebih dari batas kuota" # pesan pop up
            #                     }
            #         }

    @api.depends('manifest_travel_line', 'quota')
    def _get_manifest_count(self):
        for r in self:
            r.remaining_seats = r.quota - len(r.manifest_travel_line)

    @api.onchange('package_id')
    def _onchange_update_hpp_line(self):
        for package in self:
            total = 0
            hpp_list = [(5, 0, 0)]
            for rec in self.env['mrp.bom.line'].search([('bom_id', '=', package.package_id.id)]):
                subtotal = rec.product_id.list_price * rec.product_qty
                hpp_list.append([0, 0, {
                    'name': rec.product_id.id,
                    'product_qty': rec.product_qty,
                    'product_uom': rec.product_uom_id.id,
                    'price': rec.product_id.list_price,
                    'price_subtotal': subtotal
                }])
                total += subtotal
            package.amount_total = total
            package.hpp_line = hpp_list

    @api.model
    def create(self, vals):
        if vals.get('name',  _('/')) == _('/'):
            vals['name'] = self.env['ir.sequence'].next_by_code('travel.package') or _('/')
        result = super(TravelPackage, self).create(vals)
        return result

    
    def action_confirm(self):
        return self.write({'state': 'confirm'})
        return

    
    def action_done(self):
        return self.write({'state': 'done'})
        return

    
    def action_update(self):
        manifest_list = [(5, 0, 0)]
        for package in self:
            for rec in package.env['sale.order'].search([('package_id', '=', package.id)]):
                for data in rec.env['manifest.lines'].search([('order_id', '=', rec.id)]):
                    manifest_list.append([0, 0, {
                        'name': data.id,
                        'agent': self._uid,
                    }])
            package.manifest_travel_line = manifest_list

    # 
    # def action_update(self):
    #     for package in self:
    #         manifest_list = [(5, 0, 0)]
    #         for rec in package.env['sale.order'].search([('package_id', '=', package.id)]):
    #             for n in rec.manifest_line:
    #                 manifest_list.append([0, 0, {
    #                     'gender': ,
    #                     'pass_name': ,
    #                     'pass_no': ,
    #                     'ktp_no': ,
    #                     'date_birth': ,
    #                     'place_birth': ,
    #                     'date_isue': ,
    #                     'date_exp': ,
    #                     'imigrasi': ,
    #                     'age': ,
    #                     'room_type': ,
    #                     'agent': self._uid,
    #                 }])
    #         package.manifest_line = manifest_list

    
    def action_to_draft(self):
        return self.write({'state': 'draft'})
        return

    
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s# %s' % (rec.name, rec.product_id.name)))
        return res

    @api.depends('hpp_line.price_subtotal')
    def _compute_get_price_total(self):
        for rec in self:
            total = 0
            for line in rec.hpp_line:
                total += line.price_subtotal
            rec.amount_total = total
    