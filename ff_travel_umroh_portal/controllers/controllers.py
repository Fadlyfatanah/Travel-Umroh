# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
_logger = logging.getLogger(__name__)

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        SaleOrder = request.env['sale.order']
        MySaleOrder = SaleOrder.search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),\
            ('state', 'in', ['sent', 'sale'])])
        
        TravelPackage = request.env['travel.package']
        if 'package_count' in counters:
            values['package_count'] = TravelPackage.search_count([
                # ('id', 'in', package_ids),
                ('state', 'in', ['confirm', 'done'])
            ]) if TravelPackage.check_access_rights('read', raise_exception=False) else 0
        return values

    def _package_get_page_view_values(self, package, access_token, **kw):
        partner = request.env.user.partner_id
        order_id = request.env['sale.order'].search([('message_partner_ids', 'child_of',\
        [partner.commercial_partner_id.id]), ('state', 'in', ['sent', 'sale'])])
        manifest_line = request.env['manifest.lines'].sudo().search([('order_id', '=', order_id.id)])
        airline_line = request.env['airline.lines'].sudo().search([('travel_id', '=', package.id)])
        hotel_line = request.env['hotel.lines'].sudo().search([('travel_id', '=', package.id)])
        schedule_line = request.env['schedule.lines'].sudo().search([('travel_id', '=', package.id)])
        values = {
            'page_name': 'package',
            'package': package,
            'manifest_line': manifest_line,
            'airline_line': airline_line,
            'hotel_line': hotel_line,
            'schedule_line': schedule_line,
            'user': request.env.user,
        }
        return self._get_page_view_values(package, access_token, values, 'my_package_history', False, **kw)

    @http.route(['/my/packages', '/my/packages/page/<int:page>'], auth='public', type='http', website=True, csrf=False)
    def portal_my_packages(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        TravelPackage = request.env['travel.package']
        
        # Search package from sale order
        SaleOrder = request.env['sale.order']
        MySaleOrder = SaleOrder.search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),\
            ('state', 'in', ['sent', 'sale'])])

        domain = [
            ('state', 'in', ['confirm', 'done'])
        ]

        searchbar_sortings = {
            'departure_date': {'label': _('Departure Date'), 'order': 'departure_date'},
            'return_date': {'label': _('Return Date'), 'order': 'return_date'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'state': {'label': _('Status'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        package_count = TravelPackage.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/packages",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=package_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        packages = TravelPackage.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_package_history'] = packages.ids[:100]

        values.update({
            'date': date_begin,
            'packages': packages.sudo(),
            'page_name': 'package',
            'pager': pager,
            'default_url': "/my/packages/",
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("ff_travel_umroh_portal.portal_my_packages", values)

    @http.route(['/my/package/<int:package_id>'], type='http', auth="public", website=True)
    def portal_my_package(self, package_id=None, access_token=None, **kw):
        try:
            package_sudo = self._document_check_access('travel.package', package_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._package_get_page_view_values(package_sudo, access_token, **kw)
        
        return request.render("ff_travel_umroh_portal.portal_my_package", values)

class GetDropDown(http.Controller):
    @http.route('/pendaftaran/data-diri/getnegara', auth="public", type="http", csrf=False)
    def getnegara(self, **values):
        text = "<option value=''>-Pilih Negara-</option>"
        for pr in request.env['res.country'].sudo().search([]):
            text = text + "<option value='"+str(pr.id)+"'>"+str(pr.name)+"</option>"
        return text
    
    @http.route('/pendaftaran/data-diri/getNegarasubProvinsi', auth="public", type="http", csrf=False)
    def getNegarasubProvinsi(self, **values):
        tempRequest = request.httprequest
        getAttr = tempRequest.values
        idNegara = getAttr.get('negara',False)
        getProvinsi = request.env['res.country.state'].sudo()
        baris = getProvinsi.search([('country_id','=',int(idNegara))])
        text = "<option value=''>-Pilih Provinsi-</option>"
        for ll in baris:
            text = text + "<option value='"+str(ll.id)+"'>"+str(ll.name)+"</option>"
        return text
    
    @http.route('/pendaftaran/data-diri/getNegarasubProvinsisubKota', auth="public", type="http", csrf=False)
    def getNegarasubProvinsisubKota(self, **values):
        tempRequest = request.httprequest
        getAttr = tempRequest.values
        idprovinsi = getAttr.get('provinsi',False)
        getKota = request.env['res.state.city'].sudo()
        baris = getKota.search([('state_id','=',int(idprovinsi))])
        text = "<option value=''>-Pilih Kota/Kabupaten-</option>"
        for ll in baris:
            text = text + "<option value='"+str(ll.id)+"'>"+str(ll.name)+"</option>"
        return text
    
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
        return request.render("ff_travel_umroh_portal.jamaah", render_values)
    
    @http.route(['/shop/jamaah/delete'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah_delete(self, **kw):
        errors = {}
        order = request.website.sale_get_order()
        package_ids = order.order_line.mapped('product_id')\
            .mapped('product_template_attribute_value_ids').mapped('product_attribute_value_id')\
            .mapped('package_id')
        # partner_id = int(kw.get('partner_id')) if kw.get('partner_id', False) else 0
        # package_id = int(kw.get('package_id')) if kw.get('package_id', False) else 0
        manifest = int(kw.get('manifest')) if kw.get('manifest', False) else 0
        manifest_line = request.env['manifest.lines'].sudo().browse(manifest)
        manifest_line.sudo().unlink()

        render_values = {
            'website_sale_order': order,
            'package_ids': package_ids,
            'error': errors,
        }
        return request.render("ff_travel_umroh_portal.jamaah", render_values)
    
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
            return request.render("ff_travel_umroh_portal.jamaah_selection", render_values)
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
                'title': partner_id.title.id,
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
        return request.render("ff_travel_umroh_portal.jamaah", render_values)

    @http.route(['/shop/jamaah/register'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah_register(self, **kw):
        values = kw
        Partner = request.env['res.partner']
        order = request.website.sale_get_order()
        partner_id = Partner.browse(int(kw.get('partner_id', order.partner_id.id)))
        title_id = request.env['res.partner.title'].sudo().search([('type', '=', 'person')])
        blood_type = request.env['res.blood.type'].sudo().search([])
        clothes_size = request.env['res.clothes.size'].sudo().search([])
        education = request.env['res.education'].sudo().search([])
        marital_status = request.env['res.marital.status'].sudo().search([])
        errors = {}
        if partner_id:
            values = partner_id

        render_values = {
            'website_sale_order': order,
            'partner_id': partner_id.id,
            'title_id': title_id,
            'blood_type': blood_type,
            'clothes_size': clothes_size,
            'education': education,
            'marital_status': marital_status,
            'jamaah': values,
            'error': errors,
            'callback': kw.get('callback'),
        }
        return request.render("ff_travel_umroh_portal.jamaah_register", render_values)
    
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
            "title": int(kw.get('title', False)),
            "father_name": kw.get('father_name', False),
            "mother_name": kw.get('mother_name', False),
            "job": kw.get('job', False),
            "blood_type": kw.get('blood_type', False),
            "marital_status": kw.get('marital_status', False),
            "education": kw.get('education', False),
            "clothes_size": kw.get('clothes_size', False),
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
            "mahram": kw.get('mahram_id', False),
            "notes": kw.get('notes', False),
            "agent": kw.get('agent_id', False),
            "room_type": kw.get('room_type', False),
        }
        request.env['manifest.lines'].sudo().create(manifest_value)

        render_values = {
            'website_sale_order': order,
            'package_ids': package_ids,
            'callback': kw.get('callback'),
        }
        return request.render("ff_travel_umroh_portal.jamaah", render_values)
