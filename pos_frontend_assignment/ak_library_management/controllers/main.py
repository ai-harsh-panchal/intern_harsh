# -*- coding: utf-8 -*-

import base64
import io
import zipfile

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
        partners = request.env['res.partner'].sudo().search([])
        return http.request.render('ak_library_management.res_partner_template', {
            'partners': partners
        })

    @http.route('/partner/<string:slug>-<int:partner_id>/', type='http', auth="public", website=True)
    def partner_details(self, partner_id):
        """
        this function render the product details template
        return: Rendered HTML response containing the partner details.
        """
        contact = request.env['res.partner'].sudo().browse(partner_id)
        return request.render('ak_library_management.partner_detail_template', {
            'contact': contact
        })

    @http.route('/partner/save', type='json', auth='user', methods=['POST'])
    def save_partner(self, **kwargs):
        """
        this function is used edit and store the contact details in res partner model
        return : dictionary
        """

        partner_id = kwargs.get('partner_id')
        customer_name = kwargs.get('name')
        customer_email = kwargs.get('email')
        website = kwargs.get('website')
        customer_phone = kwargs.get('phone')
        customer_vat = kwargs.get('vat')
        customer_mobile = kwargs.get('mobile')

        existing_partners = request.env['res.partner'].sudo().search([
            ('id', '!=', partner_id),
            '|', ('email', '=', customer_email), ('phone', '=', customer_phone)
        ])

        if existing_partners:
            return {'error': 'Details are already exists'}
        partner = request.env['res.partner'].sudo().browse(partner_id)

        if partner:
            partner.write({
                'name': customer_name,
                'email': customer_email,
                'website': website,
                'phone': customer_phone,
                'vat': customer_vat,
                'mobile': customer_mobile,
            })
            return {'success': True}
        return {'success': False, 'error': 'Partner not found'}

    @http.route('/fetch_customer_details', type='http', auth='public', website=True)
    def fetch_customer_details_form_json(self):
        """
        this function only just render customer form using http type
        param : self
        return : render customer template
        """
        return http.request.render('ak_library_management.customer_fetch_template_page')

    @http.route('/fetch_customer', type='json', auth='public')
    def fetch_customer(self, email):
        """
        this function is use for get the data of particular customer on
        basis on email using json type
        param : self, email
        return : customer details (dict)
        """
        customer = request.env['res.partner'].search([('email', '=', email)])
        if customer:
            return {
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.contact_address,
            }

    @http.route('/download_product_image/<int:product_id>', type='http', auth='public')
    def download_product_image(self, product_id, **kwargs):
        """
        this function is used to download the product image if the product have
        one image then it will directly download otherwise it will generate zip file
        param : self, product_id
        return : binary data
        """
        product = request.env['product.template'].sudo().browse(product_id)
        image_ids = product.product_template_image_ids
        if len(image_ids) > 1:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for image in image_ids:
                    image_data = base64.b64decode(image.image_1920)
                    image_filename = f"{product.name}_{image.id}"
                    zip_file.writestr(image_filename, image_data)
            zip_buffer.seek(0)
            return request.make_response(zip_buffer.getvalue(), headers=[
                ('Content-Type', 'application/zip'),
                ('Content-Disposition', f'attachment; filename="{product.name}_images.zip"')
            ])
        else:
            image_data = product.image_1920 or product.product_template_image_ids.image_1920
            if image_data:
                image_data = base64.b64decode(image_data)
                filename = f"image_{product.name}"
                return request.make_response(image_data, headers=[
                    ('Content-Type', 'image/jpeg'),
                    ('Content-Disposition', f'attachment; filename="{filename}"')
                ])

    @http.route('/customer/orders', type='http', auth='user', website=True)
    def customer_orders(self):
        user = request.env.user
        customer_id = user.partner_id.id
        customer = request.env['res.partner'].sudo().browse(customer_id)

        sale_orders = request.env['sale.order'].sudo().search([('partner_id', '=', customer_id)])
        total_invoices = len([order for order in sale_orders if order.state == 'posted'])
        total_quotations = len(
            sale_orders.filtered(lambda order: order.state == 'draft'))
        total_delivered = len(sale_orders.filtered(lambda order: order.state == 'done'))


        total_invoices_all = len(request.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')
        ]))

        total_unpaid = request.env['account.move'].sudo().search_count([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'draft')
        ])

        total_quotations_all = len(request.env['sale.order'].sudo().search([
            ('state', '=', 'draft')
        ]))

        total_deliveries = len(request.env['stock.picking'].sudo().search([
            ('state', '=', 'done')
        ]))
        return request.render('ak_library_management.customer_orders_template', {
            'customer': customer,
            'sale_orders': sale_orders,
            'total_invoices': total_invoices,
            'total_quotations': total_quotations,
            'total_delivered': total_delivered,
            'total_invoices_all': total_invoices_all,
            'total_unpaid': total_unpaid,
            'total_quotations_all': total_quotations_all,
            'total_deliveries': total_deliveries,
        })

    @http.route('/customer/orders', type='http', auth='user', website=True)
    def dashboard(self):

        total_invoices = request.env['account.move'].sudo().search([
            ('move_type', '=', 'out_invoice')
        ])
        total_amount_due = sum(invoice.amount_total for invoice in total_invoices if invoice.state == 'open')
        total_amount_paid = sum(invoice.amount_total for invoice in total_invoices if invoice.state == 'paid')
        total_amount_overdue = sum(invoice.amount_total for invoice in total_invoices if invoice.state == 'not_paid')

        total_quotations = request.env['sale.order'].sudo().search_count([
            ('state', '=', 'draft')
        ])
        total_confirmed_quotations = request.env['sale.order'].sudo().search_count([
            ('state', '=', 'sale')
        ])
        total_cancelled_quotations = request.env['sale.order'].sudo().search_count([
            ('state', '=', 'cancel')
        ])

        total_deliveries = request.env['stock.picking'].sudo().search_count([])
        total_completed_deliveries = request.env['stock.picking'].sudo().search_count([
            ('state', '=', 'done')
        ])
        total_pending_deliveries = total_deliveries - total_completed_deliveries

        return request.render('ak_library_management.customer_orders_template', {
            'total_amount_due': total_amount_due,
            'total_amount_paid': total_amount_paid,
            'total_amount_overdue': total_amount_overdue,
            'total_quotations': total_quotations,
            'total_confirmed_quotations': total_confirmed_quotations,
            'total_cancelled_quotations': total_cancelled_quotations,
            'total_deliveries': total_deliveries,
            'total_completed_deliveries': total_completed_deliveries,
            'total_pending_deliveries': total_pending_deliveries,
        })
