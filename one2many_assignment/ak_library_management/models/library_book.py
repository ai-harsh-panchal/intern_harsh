# -*- coding: utf-8 -*-
from odoo import models, fields

class Book(models.Model):
    """
    Model representing a book details in the library.
    """
    _name = 'library.book'
    _description = 'Book Model'

    name = fields.Char(string='Book Title', required=True)  # Title of the book
    author = fields.Char(string='Author Name')  # Author of the book
    Library_id = fields.Many2one('library.library', string='Library')  # Library where the book is stored
    isbn = fields.Char(string='ISBN Number')  # unique identification number of the book
    publication_date = fields.Date(string='Date of Publication')  # Publication date of the book
    category_id = fields.Many2one('library.category', string='Book Category')  # Category of the book
    description = fields.Text(string='Book Summary')  # Summary of the book
    tag_ids = fields.Many2many('library.tag', string='Tags', related='category_id.tag_ids',
                               readonly=False)  # Tags associated with the book
    state = fields.Selection([
        ('available', 'Available'),  # Book is available for borrowing
        ('borrowed', 'Borrowed'),  # Book is currently borrowed
    ], default='available', string='Status')  # Default status is 'available'

    member_ids = fields.One2many('library.member', 'book_id',
                                 string='Member Assign')  # Members who have borrowed the book

    def statusbar(self):
        """
        Returns the current status of the book.
        Returns:
            str: The status of the book, either 'Available' or 'Borrowed'.
        """
        if self.state == 'available':
            return 'Available'  # Book is available
        else:
            return 'Borrowed'  # Book is borrowed
