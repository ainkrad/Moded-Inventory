# -*- coding: utf-8 -*-
from odoo import http

# class LoanApplication(http.Controller):
#     @http.route('/loan_application/loan_application/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/loan_application/loan_application/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('loan_application.listing', {
#             'root': '/loan_application/loan_application',
#             'objects': http.request.env['loan_application.loan_application'].search([]),
#         })

#     @http.route('/loan_application/loan_application/objects/<model("loan_application.loan_application"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('loan_application.object', {
#             'object': obj
#         })