# -*- coding: utf-8 -*-
from odoo import http

# class Hr-custom-employee-id(http.Controller):
#     @http.route('/hr-custom-employee-id/hr-custom-employee-id/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr-custom-employee-id/hr-custom-employee-id/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr-custom-employee-id.listing', {
#             'root': '/hr-custom-employee-id/hr-custom-employee-id',
#             'objects': http.request.env['hr-custom-employee-id.hr-custom-employee-id'].search([]),
#         })

#     @http.route('/hr-custom-employee-id/hr-custom-employee-id/objects/<model("hr-custom-employee-id.hr-custom-employee-id"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr-custom-employee-id.object', {
#             'object': obj
#         })