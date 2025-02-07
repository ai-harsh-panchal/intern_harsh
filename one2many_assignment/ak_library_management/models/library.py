# -*- coding: utf-8 -*-

from odoo import models, fields

class Library(models.Model):
    """
    Model representing a details in the library.
    """
    _name = 'library.library'
    _description = 'library Model'

    name = fields.Char(string='Name', required=True)
    book_ids = fields.One2many(comodel_name='library.book', inverse_name='library_id', string='Books')
    location = fields.Char(string='Location')  
    capacity = fields.Integer(string='Capacity')  
    notes = fields.Text(string='Notes')  
