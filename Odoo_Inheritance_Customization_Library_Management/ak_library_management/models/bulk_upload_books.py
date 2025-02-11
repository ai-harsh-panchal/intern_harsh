# -*- coding: utf-8 -*-

from odoo import models, fields


class BulkUploadBooks(models.TransientModel):
    """
    this is a transient model in which it is used to upload multiple books
    using orm create method
    """
    _name = 'bulk.upload.books'
    _description = 'Bulk Upload Books'

    book_names = fields.Text(string='Book Names')
    author_id = fields.Many2one('res.partner', string='Author', required=True)

    def create_product(self):
        book_names = self.book_names.split(',')

        for book_name in book_names:
            book_name = book_name.strip()

            existing_product = self.env['product.template'].search([('name', '=', book_name)], limit=1)

            if existing_product:
                continue

            self.env['product.template'].create({
                'name': book_name,
                'author': self.author_id.id
            })
