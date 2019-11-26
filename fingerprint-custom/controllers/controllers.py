# -*- coding: utf-8 -*-
from odoo import http

# class Fingerprint-custom(http.Controller):
#     @http.route('/fingerprint-custom/fingerprint-custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fingerprint-custom/fingerprint-custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fingerprint-custom.listing', {
#             'root': '/fingerprint-custom/fingerprint-custom',
#             'objects': http.request.env['fingerprint-custom.fingerprint-custom'].search([]),
#         })

#     @http.route('/fingerprint-custom/fingerprint-custom/objects/<model("fingerprint-custom.fingerprint-custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fingerprint-custom.object', {
#             'object': obj
#         })