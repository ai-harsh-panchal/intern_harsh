# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request
import zipfile
import io


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
        """
        this function only just render customer form using http type
        """
        return http.request.render('ak_library_management.customer_fetch_template')

    @http.route('/fetch_customer', type='json', auth='public')
    def fetch_customer(self, email):
        """
        this function is use for get the data of particular customer on
        basis on email using json type
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