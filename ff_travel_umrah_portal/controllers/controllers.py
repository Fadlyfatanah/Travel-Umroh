# -*- coding: utf-8 -*-
import json

from odoo import http, _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleTravel(WebsiteSale):

    @http.route(['/shop/jamaah'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah(self, **kw):
        errors = {}
        order = request.website.sale_get_order()
        package_ids = order.order_line.mapped('product_id')\
            .mapped('product_template_attribute_value_ids').mapped('product_attribute_value_id')\
            .mapped('package_id')

        render_values = {
            'website_sale_order': order,
            'package_ids': package_ids,
            'error': errors,
        }
        return request.render("ff_travel_umrah_portal.jamaah", render_values)
    
    @http.route(['/shop/jamaah/delete'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah_delete(self, **kw):
        errors = {}
        order = request.website.sale_get_order()
        package_ids = order.order_line.mapped('product_id')\
            .mapped('product_template_attribute_value_ids').mapped('product_attribute_value_id')\
            .mapped('package_id')
        manifest = int(kw.get('manifest')) if kw.get('manifest', False) else 0
        manifest_line = request.env['manifest.lines'].sudo().browse(manifest)
        manifest_line.sudo().unlink()

        render_values = {
            'website_sale_order': order,
            'package_ids': package_ids,
            'error': errors,
        }
        return request.render("ff_travel_umrah_portal.jamaah", render_values)
    
    @http.route(['/shop/jamaah/selection'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah_selection(self, **kw):
        order = request.website.sale_get_order()
        jamaah_ids = order.partner_id.child_ids.filtered(lambda c: c.jamaah == True)
        if jamaah_ids:
            render_values = {
                "website_sale_order": order,
                "jamaah_ids": jamaah_ids,
                "package_id": kw.get('package_id', False),
            }
            return request.render("ff_travel_umrah_portal.jamaah_selection", render_values)
        else:
            return self.jamaah_register(kw)
    
    @http.route(['/shop/jamaah/selection/list'], type='http', methods=['GET'], auth="public", website=True, sitemap=False, csrf=False)
    def jamaah_selection_list(self, **kw):
        order = request.website.sale_get_order()
        jamaah_ids = order.partner_id.child_ids
        if jamaah_ids:
           val = {"jamaah_ids": []}
           for jamaah in jamaah_ids:
               read_field = ["name", "ktp_no", "mobile", "phone"]
               val["jamaah_ids"].append(jamaah.read(read_field)[0])
           return json.dumps(val)
        else:
            return self.jamaah_register(kw)
    
    @http.route(['/shop/jamaah/selection/add'], type='http', methods=['POST'], auth="public", website=True, sitemap=False, csrf=False)
    def jamaah_selection_add(self, **kw):
        order = request.website.sale_get_order()
        package_ids = order.order_line.mapped('product_id')\
            .mapped('product_template_attribute_value_ids').mapped('product_attribute_value_id')\
            .mapped('package_id')
        package_id = int(kw.get('package_id'))if kw.get('package_id', False) else False
        for key in kw:
            if kw[key] != 'on':
                continue
            partner_id = request.env['res.partner'].browse(int(key))
            manifest_name = order.manifest_line.filtered(lambda m: m.travel_id.id == package_id).mapped('name')
            val = {
                'order_id': order.id,
                'name': partner_id.id,
                'ktp_no': partner_id.ktp_no,
                'date_birth': partner_id.date_birth,
                'place_birth': partner_id.place_birth,
                'pass_no': partner_id.pass_no,
                'date_exp': partner_id.date_exp,
                'pass_name': partner_id.pass_name,
                'date_isue': partner_id.date_isue,
                'imigrasi': partner_id.imigrasi,
                'title_id': partner_id.title_id.id,
                'gender': partner_id.gender,
                'travel_id': package_id,
            }
            if partner_id.id in manifest_name.ids:
                get_manifest_by_partner = order.manifest_line\
                    .filtered(lambda m: m.name.id == partner_id.id and m.travel_id.id == package_id)
                if len(get_manifest_by_partner.ids) == 1:
                    get_manifest_by_partner.sudo().write(val)
            else:
                order.sudo().write({'manifest_line': [(0,0,val)]})
                
        for line in order.manifest_line:
            line.calculate_age()
        
        render_values = {
            'website_sale_order': order,
            'package_ids': package_ids,
            'callback': kw.get('callback'),
        }
        return request.render("ff_travel_umrah_portal.jamaah", render_values)

    @http.route(['/shop/jamaah/register'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah_register(self, **kw):
        values = kw
        Partner = request.env['res.partner']
        order = request.website.sale_get_order()
        partner_id = Partner.browse(int(kw.get('partner_id', order.partner_id.id)))
        title_id = request.env['res.partner.title'].sudo().search([('type', '=', 'person')])
        blood_type = request.env['res.blood.type'].sudo().search([])
        clothes_size_id = request.env['res.clothes.size'].sudo().search([])
        education_id = request.env['res.education'].sudo().search([])
        marital_status_id = request.env['res.marital.status'].sudo().search([])
        errors = {}
        if partner_id:
            values = partner_id

        render_values = {
            'website_sale_order': order,
            'partner_id': partner_id.id,
            'title_id': title_id,
            'blood_type': blood_type,
            'clothes_size_id': clothes_size_id,
            'education_id': education_id,
            'marital_status_id': marital_status_id,
            'jamaah': values,
            'error': errors,
            'callback': kw.get('callback'),
        }
        return request.render("ff_travel_umrah_portal.jamaah_register", render_values)
    
    @http.route(['/shop/jamaah/register/add'], type='http', auth="public", website=True, sitemap=False)
    def add_new_jamaah(self, **kw):
        order = request.website.sale_get_order()
        package_ids = order.order_line.mapped('product_id')\
            .mapped('product_template_attribute_value_ids').mapped('product_attribute_value_id')\
            .mapped('package_id')
        partner_value = {
            "name": kw.get('name', False),
            "ktp_no": kw.get('ktp_no', False),
            "place_birth": kw.get('place_birth', False),
            "date_birth": kw.get('date_birth', False),
            "street": kw.get('street', False),
            "street2": kw.get('street2', False),
            "city": kw.get('city', False),
            "phone": kw.get('phone', False),
            "mobile": kw.get('mobile', False),
            "email": kw.get('email', False),
            "title_id": int(kw.get('title_id', False)),
            "father_name": kw.get('father_name', False),
            "mother_name": kw.get('mother_name', False),
            "job": kw.get('job', False),
            "blood_type": kw.get('blood_type', False),
            "marital_status_id": kw.get('marital_status_id', False),
            "education_id": kw.get('education_id', False),
            "clothes_size_id": kw.get('clothes_size_id', False),
            "pass_no": kw.get('pass_no', False),
            "pass_name": kw.get('pass_name', False),
            "date_isue": kw.get('date_isue', False),
            "date_exp": kw.get('date_exp', False),
            "imigrasi": kw.get('imigrasi', False),
            "parent_id": int(kw.get('partner_id', False)),
            "jamaah": True,
        }

        partner_id = request.env['res.partner'].sudo().create(partner_value)

        manifest_value = {
            "name": partner_id.id,
            "order_id": order.id,
            "mahram_id": kw.get('mahram_id', False),
            "notes": kw.get('notes', False),
            "agent_id": kw.get('agent_id', False),
            "room_type": kw.get('room_type', False),
        }
        request.env['manifest.lines'].sudo().create(manifest_value)

        render_values = {
            'website_sale_order': order,
            'package_ids': package_ids,
            'callback': kw.get('callback'),
        }
        return request.render("ff_travel_umrah_portal.jamaah", render_values)
