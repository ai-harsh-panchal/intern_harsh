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
    product_create = fields.Boolean(string='Create Products', default=False)
    book_count = fields.Integer(compute="compute_count_book")

    def create_product(self):
        """
        this function create a book record in product.template model and also
        check the if duplicate record value get then it will not create the record
        """
        book_names = self.book_names.split(',')
        print(f'book name---- split-- {book_names}')

        for book_name in book_names:
            book_name = book_name.strip()
            print(f'book name----strip-- {book_names}')

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
        this function is used to revert the changes in which if we create a record and
        want to do delete it record then we i call this function
        """
        for book in self.env['product.template'].search([('name', '=', self.book_names.split(','))]):
            book.unlink()
        self.product_create = False

    def compute_count_book(self):
        """
        this function is just count the book for smart button only
        """
        self.book_count = 0
        book_names_list = self.book_names.split(',')
        for book in book_names_list:
            book = book.strip()
            self.book_count += self.env['product.template'].search_count([('name', '=', book)])

    def action_book_list(self):
        """
        This function is used to open a form view when record is 1
         if records are multiple records then open list view
        """
        book_records = self.env['product.template'].search([('name', 'in', self.book_names.split(','))])
        if len(book_records) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Book Detail',
                'res_model': 'product.template',
                'res_id': book_records.id,
                'view_mode': 'form',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Bulk Book Uploaded',
                'view_mode': 'list',
                'res_model': 'product.template',
                'domain': [('name', 'in', self.book_names.split(','))],
                'context': {'create': False}
            }
