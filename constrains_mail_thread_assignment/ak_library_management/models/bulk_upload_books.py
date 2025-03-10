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
    _rec_name = 'book_names'

    book_names = fields.Text(string='Book Names')
    author_id = fields.Many2one('res.partner', string='Author', required=True)
    product_create = fields.Boolean(string='Create Products')
    book_count = fields.Integer(compute="compute_count_book")
    category_id = fields.Many2one(comodel_name='library.category', string='Category')
    price = fields.Float(string='Price')

    def action_create_product(self):
        """
        this function create a book record in product.template model and also
        check the if duplicate record value get then it will not create the record
        parameter: self
        return: None
        """
        for book_name in self.book_names.split(','):
            book_name.strip()
            if not self.env['product.template'].search([('name', '=', book_name)]):
                products = self.env['product.template'].create({
                    'name': book_name,
                    'author': self.author_id.name
                })
                self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"{book_name} is created as product.",
                })
            self.product_create = True

    def action_revert_changes(self):
        """
        Reverts changes by deleting records of books based on their names.
        parameter: self
        return: None
        """
        single_book = self.book_names.split(',')
        self.env["product.template"].search([("name", "=", single_book)]).unlink()
        for book_name in single_book:
            book_name = book_name.strip()
            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"{book_name} is deleted.",
                })

        self.product_create = False

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
