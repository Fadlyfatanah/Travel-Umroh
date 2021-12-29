# -*- coding: utf-8 -*-
from odoo import http

# class AsbTravelUmroh(http.Controller):
#     @http.route('/xyz_travel_umroh/xyz_travel_umroh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/xyz_travel_umroh/xyz_travel_umroh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('xyz_travel_umroh.listing', {
#             'root': '/xyz_travel_umroh/xyz_travel_umroh',
#             'objects': http.request.env['xyz_travel_umroh.xyz_travel_umroh'].search([]),
#         })

#     @http.route('/xyz_travel_umroh/xyz_travel_umroh/objects/<model("xyz_travel_umroh.xyz_travel_umroh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('xyz_travel_umroh.object', {
#             'object': obj
#         })