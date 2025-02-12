# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Library(models.Model):
    """
    Model representing details in the library.
    """
    _name = 'library.library'
    _description = 'Library Model'

    name = fields.Char(string='Name', required=True)
    book_ids = fields.Many2many(
        comodel_name='product.template',
        string='Books',
        domain=[('is_library_book', '=', True)]
    )
    location = fields.Char(string='Location')
    capacity = fields.Integer(string='Capacity')
    notes = fields.Text(string='Notes')
    book_count = fields.Integer(compute='compute_book_count')

    @api.depends('book_ids')
    def compute_book_count(self):
        """
        this function is counting the number of books
        which are borrowed
        """
        for rec in self:
            borrowed_books = rec.book_ids.filtered(lambda book: book.status == 'borrowed')
            rec.book_count = len(borrowed_books)


    def action_get_books_record(self):
        """
        this function perfrom action when i click on button it display the
        list in which it contain only borrowed book
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Allocated Books',
            'view_mode': 'list',
            'res_model': 'product.template',
            'domain': [('id', 'in', self.book_ids.ids), ('status', '=', 'borrowed')],
            'context': {'create': False}
        }
