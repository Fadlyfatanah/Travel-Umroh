# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Travel Package'
    _inherit = ['mail.thread', 'portal.mixin']

    name = fields.Char(required=True, copy=False, readonly=True, index=True, default=lambda self: _('/'), size=10)
    departure_date = fields.Date(required=True, string='Departure Date', size=8)
    return_date = fields.Date(required=True, string='Return Date', size=8)
    quota = fields.Integer('Quota', size=3)
    hotel_line = fields.One2many('hotel.line', 'travel_id', string='Hotel')
    airlines_line = fields.One2many('airline.line', 'travel_id', string='Airline')
    equipment_line = fields.One2many('equipment.line', 'travel_id', string='Equipment')
    schedule_line = fields.One2many('schedule.line', 'travel_id', string='Schedule')
    hpp_line = fields.One2many('hpp.line', 'travel_id', string='HPP')
    remaining_seats = fields.Integer(compute='_compute_remaining_seats', readonly=True)
    quota_progress = fields.Float(compute='_compute_quota_progress')
    manifest_line = fields.One2many('manifest.line', 'travel_id', readonly=True, string='Manifest')
    company_id = fields.Many2one('res.company', string='Company', default=1)
    currency_id = fields.Many2one("res.currency", related='company_id.currency_id', string="Currency", readonly=True)
    muthawif_id = fields.Many2one('res.partner', string='Muthawif', domain=[('muthawif', '=', True)])
    jamaah_count = fields.Integer('Jamaah', compute='_compute_get_price_total')
    subtotal = fields.Monetary('Subtotal', compute='_compute_get_price_total')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_compute_get_price_total')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('open', 'Open'),
        ('done', 'Done'),
    ], default='draft', string='Status')

    @api.depends('quota', 'manifest_line')
    def _compute_quota_progress(self):
        for r in self:
            r.quota_progress = 0
            if len(r.manifest_line) <= r.quota and r.quota > 0:
                r.quota_progress = 100.0 * (len(r.manifest_line) / r.quota)

    @api.depends('manifest_line', 'quota')
    def _compute_remaining_seats(self):
        for r in self:
            r.remaining_seats = r.quota - len(r.manifest_line)

    def action_update_hpp(self):
        self.ensure_one()
        hpp_list = [(5, 0, 0)]
        uom_id = self.env['uom.uom'].search([('name', '=', 'Units')], limit=1)
        if len(self.equipment_line.ids) > 0:
            for line in self.equipment_line:
                hpp_list.append((0, 0, {
                    'name': line.product_id.name,
                    'product_qty': line.product_qty,
                    'product_uom': line.product_uom.id,
                    'price': line.price,
                }))

        if len(self.airlines_line.ids) > 0:
            for line in self.airlines_line:
                hpp_list.append((0, 0, {
                    'name': line.name.name,
                    'product_qty': 1,
                    'product_uom': uom_id.id,
                    'price': line.price,
                }))

        if len(self.hotel_line.ids) > 0:
            for line in self.hotel_line:
                hpp_list.append((0, 0, {
                    'name': line.name.name,
                    'product_qty': 1,
                    'product_uom': uom_id.id,
                    'price': line.price,
                }))

        self.hpp_line = hpp_list
        subtotal = sum(self.hpp_line.mapped('price_subtotal'))
        self.subtotal = subtotal
    
    def action_update_jamaah(self):
        for rec in self.env['sale.order'].search([('state', '!=', 'draft')]):
            for n in rec.manifest_line:
                n.write({
                    'travel_id': self.id,
                })


    @api.model
    def create(self, vals):
        if vals.get('name',  _('/')) == _('/'):
            vals['name'] = self.env['ir.sequence'].next_by_code('travel.package') or _('/')
        result = super(TravelPackage, self).create(vals)
        return result
    
    def unlink(self):
        super(TravelPackage, self).unlink()
        self.delete_product_attribute_value()
    
    def action_confirm(self):
        self.action_update_hpp()
        return self.write({'state': 'confirm'})
    
    def action_open(self):
        self.action_update_hpp()
        # action to create product attribute value
        self.create_product_attribute_value()
        return self.write({'state': 'open'})
    
    def action_done(self):
        self.delete_product_attribute_value()
        return self.write({'state': 'done'})
    
    def action_to_draft(self):
        self.delete_product_attribute_value()
        return self.write({'state': 'draft'})
    
    def name_get(self):
        res = []
        for rec in self:
            departure_date = rec.departure_date.strftime('%d %b')
            return_date = rec.return_date.strftime('%d %b')
            res.append((rec.id, '%s (%s - %s)' % (rec.name, departure_date, return_date)))
        return res

    @api.depends('manifest_line', 'hpp_line')
    def _compute_get_price_total(self):
        for rec in self:
            subtotal = 0
            for hpp in rec.hpp_line:
                subtotal += hpp.price_subtotal
            rec.subtotal = subtotal
            rec.jamaah_count = len(rec.manifest_line.ids)
            rec.amount_total = rec.subtotal * rec.jamaah_count
    
    def create_product_attribute(self):
        val = {
            'name': 'Package',
            'create_variant': 'always',
            'display_type': 'select',
        }
        attribute_id = self.env['product.attribute'].create(val)
        return attribute_id

    def create_product_attribute_value(self):
        attribute_id = self.env.ref('ff_travel_umrah.product_attribute_1')
        if not attribute_id:
            attribute_id = self.create_product_attribute()
        val = {
            'name': '%s (%s - %s)' %(self.name, self.departure_date.strftime('%d %b'), self.return_date.strftime('%d %b')),
            'attribute_id': attribute_id.id,
            'is_custom': False,
            'package_id': self.id,
        }
        self.env['product.attribute.value'].create(val)

    def delete_product_attribute_value(self):
        self.env['product.attribute.value'].search([('package_id', '=', self.id)]).unlink()