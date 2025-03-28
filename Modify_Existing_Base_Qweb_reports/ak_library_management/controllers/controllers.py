#-*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class DemoController(http.Controller):
    @http.route('/demo', type='http', auth="public", website=True)
    def demo(self):
        """
        this function Renders the demo page template for the library management system.
        param : self
        return : Rendered HTML of the demo page.
        """
        return http.request.render('ak_library_management.demo_page_template',{})

    @http.route('/contacts', type='http', auth="public", website=True)
    def contact(self):
        """
        Fetches all partners (contacts) and renders them using the specified template.
        param : self
        return : Rendered HTML of the contacts page with a list of partners.
        """
        partners = request.env['res.partner'].search([])
        return http.request.render('ak_library_management.res_partner_template', {
            'partners': partners
        })

    @http.route('/partner/<string:slug>-<int:partner_id>/', type='http', auth="public", website=True)
    def partner_details(self, partner_id):
        """
        this function Fetches details of a specific partner based on the provided partner_id
        param : self
        return : renders them using the partner detail template.
        """
        contact = request.env['res.partner'].browse(partner_id)
        return request.render('ak_library_management.partner_detail_template', {
            'contact': contact
        })
