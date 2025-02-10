# -*- coding: utf-8 -*-

from odoo import models, fields

class Book(models.Model):
    """
    Model representing a book details in the library.
    """
    _name = 'library.book'
    _description = 'Book Model'

    name = fields.Char(string='Book Title', required=True)
    author = fields.Char(string='Author Name')
    library_id = fields.Many2one('library.library', string='Library')
    isbn = fields.Char(string='ISBN Number')
    publication_date = fields.Date(string='Date of Publication')
    category_id = fields.Many2one('library.category', string='Book Category')
    description = fields.Text(string='Book Summary')
    tag_ids = fields.Many2many('library.tag', string='Tags', related='category_id.tag_ids',
                               readonly=False)
