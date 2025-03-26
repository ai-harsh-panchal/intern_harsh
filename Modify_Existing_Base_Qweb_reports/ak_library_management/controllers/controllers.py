#-*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class DemoController(http.Controller):
    @http.route('/demo', type='http', auth="public", website=True)
    def demo(self):
        return http.request.render('ak_library_management.demo_page_template',{})

    @http.route('/contacts', type='http', auth="public", website=True)
    def contact(self):
        partners = request.env['res.partner'].search([])
        return http.request.render('ak_library_management.res_partner_template', {
            'partners': partners
        })

    @http.route('/partner/<int:partner_id>', type='http', auth="public", website=True)
    def partner_details(self, partner_id):
        partner = request.env['res.partner'].browse(partner_id)
        return http.request.render('ak_library_management.partner_detail_template', {
            'partner': partner
        })
