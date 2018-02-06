# -*- coding: utf-8 -*-
from odoo import http

# class SerialBrdc(http.Controller):
#     @http.route('/serial_brdc/serial_brdc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/serial_brdc/serial_brdc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('serial_brdc.listing', {
#             'root': '/serial_brdc/serial_brdc',
#             'objects': http.request.env['serial_brdc.serial_brdc'].search([]),
#         })

#     @http.route('/serial_brdc/serial_brdc/objects/<model("serial_brdc.serial_brdc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('serial_brdc.object', {
#             'object': obj
#         })