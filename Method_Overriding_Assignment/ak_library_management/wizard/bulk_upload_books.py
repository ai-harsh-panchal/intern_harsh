# -*- coding: utf-8 -*-

from odoo import models, fields


class BulkUploadBooks(models.TransientModel):
    """
    Transient model for bulk uploading multiple books simultaneously.
    This wizard facilitates the creation of multiple book records through a single interface.
    It allows users to input multiple book names and associate them with an author.
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
        parameter: self
        return: None
        """
        for record in self:
            book_names = [name.strip() for name in record.book_names.split(',') if name.strip()]
            existing_books = self.env['product.template'].search([('name', 'in', book_names)]).mapped('name')
            books_to_create = []
            for book_name in book_names:
                if book_name not in existing_books:
                    books_to_create.append({
                        'name': book_name,
                        'author': record.author_id.name
                    })
            if books_to_create:
                created_books = self.env['product.template'].create(books_to_create)
            record.product_create = True

    def revert_changes(self):
        """
        Reverts changes by deleting records of books based on their names.
        parameter: self
        return: None
        """
        for record in self:
            book_names = [name.strip() for name in record.book_names.split(',') if name.strip()]
            self.env['product.template'].search([('name', 'in', book_names)]).unlink()
            record.product_create = False

    def compute_count_book(self):
        """
        Computes the count of books for the smart button.
        parameter: self
        return: None
        """
        for record in self:
            book_names = [name.strip() for name in record.book_names.split(',') if name.strip()]
            record.book_count = self.env['product.template'].search_count([
                ('name', 'in', book_names)
            ])

    def action_book_list(self):
        """
        This function is used to open a form view when there is one record.
        If there are multiple records, it opens a list view.
        param self: Recordset of the model calling the method.
        return: A dictionary defining an action, which can either open a list view for multiple records or a form view for a single record.
        return type: dict
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
