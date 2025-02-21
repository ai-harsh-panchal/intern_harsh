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
    product_create = fields.Boolean(string='Create Products')
    book_count = fields.Integer(compute="compute_count_book")

    def create_product(self):
        """
        this function create a book record in product.template model and also
        check the if duplicate record value get then it will not create the record
        """
        book_names = self.book_names.split(',')
        for book_name in book_names:
            book_name = book_name.strip()
            existing_product = self.env['product.template'].search([('name', '=', book_name)], limit=1)
            if existing_product:
                continue
            else:
                self.env['product.template'].create({
                'name': book_name,
                'author': self.author_id.name
            })
        self.product_create = True

    def revert_changes(self):
        """
        Reverts changes by deleting records of books based on their names.
        """
        domain = [('name', 'in', self.book_names.split(','))]
        self.env['product.template'].search(domain).unlink()
        self.product_create = False

    def compute_count_book(self):
        """
        Computes the count of books for the smart button.
        """
        book_names_list = [name.strip() for name in self.book_names.split(',')]
        domain = [('name', 'in', book_names_list)]
        self.book_count = self.env['product.template'].search_count(domain)

    def action_book_list(self):
        """
        This function is used to open a form view when there is one record.
        If there are multiple records, it opens a list view.
        """
        domain = [('name', 'in', self.book_names.split(','))]
        book_records = self.env['product.template'].search(domain)

        action = {
            'name': 'Bulk Book Uploaded' if len(book_records) > 1 else 'Book Detail',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'list,form' if len(book_records) > 1 else 'form',
            'domain': domain if len(book_records) > 1 else [],
            'res_id': book_records[0].id if len(book_records) == 1 else None,
            'context': {'create': False} if len(book_records) > 1 else {},
        }
        return action

