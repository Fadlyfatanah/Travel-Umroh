# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression
_logger = logging.getLogger(__name__)

class TravelUmroh(http.Controller):
    @http.route(['/pendaftaran', '/pendaftaran/<data>', '/pendaftaran/result/<model>'], auth='public', type='http', website=True, csrf=False)
    def form_pedaftaran(self, data=False, model=False, records={}, **kwargs):
        value = {}
        Partner = request.env['res.partner'].sudo()
        Title = request.env['res.partner.title'].sudo()
        SaleOrder = request.env['sale.order'].sudo()
        TravelPackage = request.env['travel.package'].sudo()
        PaymentTerm = request.env['account.payment.term'].sudo()
        Package = request.env['travel.package'].sudo()
        User = request.env['res.users'].sudo()
        uid = request._uid
        records.update(kwargs)
        user_id = User.browse(uid)
        partner_id = user_id.partner_id
        tempRequest = request.httprequest
        getAttr = tempRequest.values

        # Domain for search jamaah
        domain = [('company_type', '=', 'person')]
        if not user_id.has_group('ff_travel_umroh.group_travel_umroh_manager') or data == 'getListMahram':
            domain.append(('parent_id', '=', partner_id.id))
        else:
            domain.append(('parent_id', '!=', False))

        if data:
            if data == 'getListJamaah':
                listJamaah = getAttr['listJamaah'] if getAttr.get('listJamaah', False) else []
                domain.append(('id', 'not in', listJamaah))
                text = "<option value='' selected='' disabled=''>Jamaah</option>"
                for rec in Partner.sudo().search(domain):
                    text = text + "<option value='"+str(rec.id)+"'>"+str(rec.name)+"</option>"
                return text
            elif data == 'getListMahram':
                jamaah_id = int(getAttr['jamaah_id']) if getAttr.get('jamaah_id', False) else False
                domain.append(('id', '!=', jamaah_id))
                jamaah_ids = Partner.search(domain)
                text = "<option value='' selected='' disabled=''>Mahram</option>"
                for rec in jamaah_ids:
                    text = text + "<option value='"+str(rec.id)+"'>"+str(rec.name)+"</option>"
                return text
            elif data == 'getDetailJamaah':
                tempRequest = request.httprequest
                getAttr = tempRequest.values
                int_id = int(getAttr['jamaah_id']) if getAttr.get('jamaah_id', False) else False
                data = {}
                if int_id:
                    jamaah = Partner.browse(int_id)
                    today = fields.Date.today()
                    born = jamaah.date_birth
                    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                    gender = dict(jamaah._fields['gender'].selection).get(jamaah.gender)
                    text = "<jamaah><div name='ktp_no'>"+str(jamaah.ktp_no)+"</div><div name='gender'>"\
                        +str(gender)+"</div><div name='age'>"+str(age)+"</div></jamaah>"
                return text
                # return xml_doc.write(file)
            elif data == 'data-diri':
                blood_type = Partner._fields['blood_type'].selection
                education = Partner._fields['education'].selection
                gender = Partner._fields['gender'].selection
                # title_person = Title.search([('type', '=', 'person')])
                value.update({
                    'blood_type': blood_type,
                    'education': education,
                    'gender': gender,
                    # 'title_person': title_person,
                })
                return http.request.render('ff_travel_umroh_portal.pendaftaran_data_diri', value)
            elif data == 'data-tambahan':
                marital_status = Partner._fields['marital_status'].selection
                clothes_size = Partner._fields['clothes_size'].selection
                value.update({
                    'marital_status': marital_status,
                    'clothes_size': clothes_size,
                })
                return http.request.render('ff_travel_umroh_portal.pendaftaran_data_tambahan', value)
            elif data == 'data-passport':
                return http.request.render('ff_travel_umroh_portal.pendaftaran_data_passport', {})
            elif data == 'data-gambar':
                return http.request.render('ff_travel_umroh_portal.pendaftaran_data_gambar', {})
            elif data == 'result':
                if model == 'respartner':
                    records.update({
                        'parent_id': uid,
                        'company_type': 'person',
                    })
                    self._check_field_before_create(records)
                    Partner.sudo().create(records)
                    return http.request.render('ff_travel_umroh_portal.pendaftaran', {})
                elif model == 'saleorder':
                    value.update({
                        'state': 'sale',
                        'partner_id': uid,
                        # 'package_id': ,
                    })
                    SaleOrder.sudo().create(value)
                    # return http.request.render('ff_travel_umroh_portal.so', {})

        else:
            package_id = TravelPackage.search([('state', '=', 'open')])
            jamaah_id = Partner.search([('company_type', '=', 'person'), ('parent_id', '=', uid)])
            # title_person = Title.search([('type', '=', 'person')])
            room_type = request.env['manifest.lines']._fields['room_type'].selection
            value.update({
                'package_id': package_id,
                'jamaah_id': jamaah_id,
                # 'title_person': title_person,
                'room_type': room_type,
                'manifest_line': SaleOrder.manifest_line
            })
            return http.request.render('ff_travel_umroh_portal.pendaftaran', value)
            
    
    def _check_field_before_create(self, res):
        Model = request.env['res.partner']
        for key in res:
            if key not in Model._fields:
                continue
            elif isinstance(Model._fields[key], fields.Many2one):
                res[key] = int(res[key])
            elif isinstance(Model._fields[key], fields.Selection):
                if isinstance(res[key], dict) and "value" in res[key]:
                    res[key] = res[key]["value"]
        return res

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        SaleOrder = request.env['sale.order']
        MySaleOrder = SaleOrder.search([('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),\
            ('state', 'in', ['sent', 'sale'])])
        
        package_ids = []
        for order in MySaleOrder:
            if order.package_id:
                package_ids.append(order.package_id.id)

        TravelPackage = request.env['travel.package']
        if 'package_count' in counters:
            values['package_count'] = TravelPackage.search_count([
                ('id', 'in', package_ids),
                ('state', 'in', ['reschedule', 'confirm', 'done'])
            ]) if TravelPackage.check_access_rights('read', raise_exception=False) else 0
        return values

    def _package_get_page_view_values(self, package, access_token, **kw):
        partner = request.env.user.partner_id
        order_id = request.env['sale.order'].search([('message_partner_ids', 'child_of',\
        [partner.commercial_partner_id.id]), ('state', 'in', ['sent', 'sale']), ('package_id', '=', package.id)])
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
        package_ids = []
        for order in MySaleOrder:
            if order.package_id:
                package_ids.append(order.package_id.id)

        domain = [
            ('id', 'in', package_ids),
            ('state', 'in', ['reschedule', 'confirm', 'done'])
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
    
class WebsiteSale(http.Controller):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        if request.website.user_id.sudo().partner_id.child_ids.ids:
            return request.redirect('/shop/jamaah')

        values = self.checkout_values(**post)

        if post.get('express'):
            return request.redirect('/shop/confirm_order')

        values.update({'website_sale_order': order})

        # Avoid useless rendering if called in ajax
        if post.get('xhr'):
            return 'ok'
        return request.render("website_sale.checkout", values)
    
    @http.route(['/shop/jamaah'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah(self, **kw):
        Partner = request.env['res.partner']
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        mode = (False, False)
        can_edit_vat = False
        values, errors = {}, {}

        partner_id = int(kw.get('partner_id', -1))

        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            mode = ('new', 'billing')
            can_edit_vat = True
        # IF ORDER LINKED TO A PARTNER
        else:
            if partner_id > 0:
                if partner_id == order.partner_id.id:
                    mode = ('edit', 'billing')
                    can_edit_vat = order.partner_id.can_edit_vat()
                else:
                    shippings = Partner.search([('id', 'child_of', order.partner_id.commercial_partner_id.ids)])
                    if order.partner_id.commercial_partner_id.id == partner_id:
                        mode = ('new', 'shipping')
                        partner_id = -1
                    elif partner_id in shippings.mapped('id'):
                        mode = ('edit', 'shipping')
                    else:
                        return Forbidden()
                if mode and partner_id != -1:
                    values = Partner.browse(partner_id)
            elif partner_id == -1:
                mode = ('new', 'shipping')
            else: # no mode - refresh without post?
                return request.redirect('/shop/checkout')

        # IF POSTED
        if 'submitted' in kw and request.httprequest.method == "POST":
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg)

            if errors:
                errors['error_message'] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw)
                # We need to validate _checkout_form_save return, because when partner_id not in shippings
                # it returns Forbidden() instead the partner_id
                if isinstance(partner_id, Forbidden):
                    return partner_id
                if mode[1] == 'billing':
                    order.partner_id = partner_id
                    order.with_context(not_self_saleperson=True).onchange_partner_id()
                    # This is the *only* thing that the front end user will see/edit anyway when choosing billing address
                    order.partner_invoice_id = partner_id
                    if not kw.get('use_same'):
                        kw['callback'] = kw.get('callback') or \
                            (not order.only_services and (mode[0] == 'edit' and '/shop/checkout' or '/shop/address'))
                    # We need to update the pricelist(by the one selected by the customer), because onchange_partner reset it
                    # We only need to update the pricelist when it is not redirected to /confirm_order
                    if kw.get('callback', '') != '/shop/confirm_order':
                        request.website.sale_get_order(update_pricelist=True)
                elif mode[1] == 'shipping':
                    order.partner_shipping_id = partner_id

                # TDE FIXME: don't ever do this
                order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
                if not errors:
                    return request.redirect(kw.get('callback') or '/shop/confirm_order')

        render_values = {
            'website_sale_order': order,
            'error': errors,
            'callback': kw.get('callback'),
        }
        # render_values.update(self._get_country_related_render_values(kw, render_values))
        return request.render("ff_travel_umroh_portal.jamaah", render_values)
    
    def checkout_redirection(self, order):
        # must have a draft sales order with lines at this point, otherwise reset
        if not order or order.state != 'draft':
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            return request.redirect('/shop')

        if order and not order.order_line:
            return request.redirect('/shop/cart')

        # if transaction pending / done: redirect to confirmation
        tx = request.env.context.get('website_sale_transaction')
        if tx and tx.state != 'draft':
            return request.redirect('/shop/payment/confirmation/%s' % order.id)
        
    @http.route(['/shop/jamaah/selection'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def jamaah_selection(self, **kw):
        render_list = []
        order = request.website.sale_get_order()
        jamaah_ids = order.partner_id.child_ids.filtered(lambda c: c.jamaah == True)
        for jamaah in jamaah_ids:
            name = jamaah.name
            label = "%s(%s), %s" %(jamaah.name, jamaah.ktp_no, jamaah.phone)
            render_list.append(
                """
                    <input id="%s" type="checkbox" name="%s" t-att-value="%s"/>
                    <label class="col-form-label" for="%s">%s</label>
                """ %("jamaah_%s" %(jamaah.id), name, jamaah.id, name, label)
            )
        if jamaah_ids:
            return request.render("ff_travel_umroh_portal.jamaah_selection", {"value": render_list})
        else:
            return self.jamaah_register(kw)
    
    @http.route(['/shop/jamaah/selection/list'], type='http', methods=['GET'], auth="public", website=True, sitemap=False, csrf=False)
    def jamaah_selection_list(self, **kw):
        order = request.website.sale_get_order()
        jamaah_ids = order.partner_id.child_ids.filtered(lambda c: c.jamaah == True)
        if jamaah_ids:
            txt = ""
            for jamaah in jamaah_ids:
                id = "jamaah_%s" %(jamaah.id)
                label = jamaah.name
                if jamaah.ktp_no:
                    label += "(%s)" %jamaah.ktp_no
                if jamaah.phone or jamaah.mobile:
                    label += ", %s" %jamaah.phone
                    label += ", %s" %jamaah.mobile
                txt += """
                    <input id="%s" type="checkbox" name="%s" t-att-value="%s"/>
                    <label class="col-form-label" for="%s">%s</label>
                    <div class="w-100"/>
                """ %(id, jamaah.id, jamaah.id, jamaah.name, label)
            return txt
        else:
            return self.jamaah_register(kw)
    
    @http.route(['/shop/jamaah/selection/add'], type='http', methods=['POST'], auth="public", website=True, sitemap=False, csrf=False)
    def jamaah_selection_add(self, **kw):
        order = request.website.sale_get_order()
        val_list = []
        keys = kw.keys()
        for key in keys:
            partner_id = request.env['res.partner'].browse(int(key))
            val_list.append({
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
                'title': partner_id.title,
                'gender': partner_id.gender,
            })
        request.env['manifest.lines'].sudo().create(val_list)
        render_values = {
            'website_sale_order': order,
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
            'callback': kw.get('callback'),
        }
        return request.render("ff_travel_umroh_portal.jamaah", render_values)