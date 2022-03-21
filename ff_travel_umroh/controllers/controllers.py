# -*- coding: utf-8 -*-
from odoo import http, fields, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression

class WebsiteForm(http.Controller):
    @http.route('/pendaftaran/<data>', auth='public', type='http', website=True, csrf=False)
    def index(self, data, records={}, **kw):
        value = {}
        records.update(kw)

        if data == 'data-diri':
            blood_type = request.env['res.partner']._fields['blood_type'].selection
            education = request.env['res.partner']._fields['education'].selection
            gender = request.env['res.partner']._fields['gender'].selection
            title = request.env['res.partner']._fields['title'].selection
            value.update({
                'blood_type': blood_type,
                'education': education,
                'gender': gender,
                'title': title,
            })
            return http.request.render('ff_travel_umroh.pendaftaran_data_diri', value)
        if data == 'data-tambahan':
            marital_status = request.env['res.partner']._fields['marital_status'].selection
            clothes_size = request.env['res.partner']._fields['clothes_size'].selection
            value.update({
                'marital_status': marital_status,
                'clothes_size': clothes_size,
            })
            return http.request.render('ff_travel_umroh.pendaftaran_data_tambahan', value)
        if data == 'data-passport':
            return http.request.render('ff_travel_umroh.pendaftaran_data_passport', {})
        if data == 'data-gambar':
            return http.request.render('ff_travel_umroh.pendaftaran_data_gambar', {})
        if data == 'result':
            records.update({
                # 'parent_id': ,
                'company_type': 'person',
            })
            self._check_field_before_create(records)
            request.env['res.partner'].sudo().create(records)
            return http.request.render('ff_travel_umroh.pendaftaran_data_diri', {})
    
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