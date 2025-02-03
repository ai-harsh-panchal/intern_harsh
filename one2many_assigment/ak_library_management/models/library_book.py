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
    isbn = fields.Char(string='ISBN Number')  # ISBN number of the book
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


class Tag(models.Model):
    """
    Model representing a tag that can be associated with books.
    """
    _name = 'library.tag'
    _description = 'Library Tag'

    name = fields.Char(string='Tag Name', required=True)  # Name of the tag
    description = fields.Text(string='Tag Description')  # Description of the tag


class Category(models.Model):
    """
    Model representing a category of books in the library.
    """
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char(string='Category Name', required=True)  # Name of the category
    description = fields.Text(string='Category Description')  # Description of the category
    tag_ids = fields.Many2many('library.tag', string='Tags')  # Tags associated with the category
