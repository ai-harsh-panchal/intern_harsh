# -*- coding: utf-8 -*-
from odoo import models, fields

class Library(models.Model):
    """
    Model representing a details in the library.
    """
    _name = 'library.library'
    _description = 'library Model'

    name = fields.Char(string='name', required=True)
    book_ids = fields.One2many(comodel_name='library.book', inverse_name='Library_id', string='Books')
    location = fields.Char(string='Location')  # Location of the book
    capacity = fields.Integer(string='Capacity')  # Capacity of the book
    notes = fields.Text(string='Notes')  # Notes about the book
