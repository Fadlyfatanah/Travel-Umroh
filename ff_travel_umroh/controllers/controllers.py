# -*- coding: utf-8 -*-
from xml.dom.minidom import parse, parseString
from odoo import http, fields, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class TravelUmroh(http.Controller):
    @http.route(['/pendaftaran', '/pendaftaran/<data>', '/pendaftaran/result/<model>'], auth='public', type='http', website=True, csrf=False)
    def form_pedaftaran(self, data=False, model=False, records={}, **kwargs):
        value = {}
        Partner = request.env['res.partner'].sudo()
        SaleOrder = request.env['sale.order'].sudo()
        TravelPackage = request.env['travel.package'].sudo()
        PaymentTerm = request.env['account.payment.term'].sudo()
        Product = request.env['product.template'].sudo()
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
                listJamaah = getAttr['listJamaah'] if getAttr.get('listJamaah', False) else False
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
                title_person = Partner._fields['title'].selection
                value.update({
                    'blood_type': blood_type,
                    'education': education,
                    'gender': gender,
                    'title_person': title_person,
                })
                return http.request.render('ff_travel_umroh.pendaftaran_data_diri', value)
            elif data == 'data-tambahan':
                marital_status = Partner._fields['marital_status'].selection
                clothes_size = Partner._fields['clothes_size'].selection
                value.update({
                    'marital_status': marital_status,
                    'clothes_size': clothes_size,
                })
                return http.request.render('ff_travel_umroh.pendaftaran_data_tambahan', value)
            elif data == 'data-passport':
                return http.request.render('ff_travel_umroh.pendaftaran_data_passport', {})
            elif data == 'data-gambar':
                return http.request.render('ff_travel_umroh.pendaftaran_data_gambar', {})
            elif data == 'result':
                if model == 'respartner':
                    records.update({
                        'parent_id': uid,
                        'company_type': 'person',
                    })
                    self._check_field_before_create(records)
                    Partner.sudo().create(records)
                    return http.request.render('ff_travel_umroh.pendaftaran', {})
                elif model == 'saleorder':
                    value.update({
                        'state': 'sale',
                        'partner_id': uid,
                        # 'package_id': ,
                    })
                    SaleOrder.sudo().create(value)
                    # return http.request.render('ff_travel_umroh.so', {})

        else:
            package_id = TravelPackage.search([('state', '=', 'confirm')])
            jamaah_id = Partner.search([('company_type', '=', 'person'), ('parent_id', '=', uid)])
            product_id = Product.search([('type', '=', 'service')])
            title_person = Partner._fields['title'].selection
            room_type = request.env['manifest.lines']._fields['room_type'].selection
            value.update({
                'package_id': package_id,
                'jamaah_id': jamaah_id,
                'product_id': product_id,
                'title_person': title_person,
                'room_type': room_type,
                'manifest_line': SaleOrder.manifest_line
            })
            return http.request.render('ff_travel_umroh.pendaftaran', value)
            
    
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
        return request.render("ff_travel_umroh.portal_my_packages", values)

    @http.route(['/my/package/<int:package_id>'], type='http', auth="public", website=True)
    def portal_my_package(self, package_id=None, access_token=None, **kw):
        try:
            package_sudo = self._document_check_access('travel.package', package_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._package_get_page_view_values(package_sudo, access_token, **kw)
        
        return request.render("ff_travel_umroh.portal_my_package", values)

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
