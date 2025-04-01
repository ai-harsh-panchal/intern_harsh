# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class CustomerController(http.Controller):

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


    @http.route('/fetch_customer_details', type='http', auth='public', website=True)
    def fetch_customer_details_form(self):
        return http.request.render('ak_library_management.customer_fetch_template')

    @http.route('/fetch_customer', type='json', auth='public')
    def fetch_customer(self, email):
        customer = request.env['res.partner'].search([('email', '=', email)])
        if customer:
            return {
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.contact_address,
            }
