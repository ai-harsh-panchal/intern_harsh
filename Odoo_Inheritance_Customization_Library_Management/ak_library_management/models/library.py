# -*- coding: utf-8 -*-

from odoo import models, fields

class Library(models.Model):
    """
    Model representing a details in the library.
    """
    _name = 'library.library'
    _description = 'library Model'

    name = fields.Char(string='name', required=True)
    book_ids = fields.Many2many(comodel_name='product.template', string='Books', domain=[('is_library_book', '=', True)])
    location = fields.Char(string='Location')
    capacity = fields.Integer(string='Capacity')
    notes = fields.Text(string='Notes')
