# -*- coding: utf-8 -*-
from odoo import models, fields

class Category(models.Model):
    """
    Model representing a category of books in the library.
    """
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char(string='Category Name', required=True)  # Name of the category
    description = fields.Text(string='Category Description')  # Description of the category
    tag_ids = fields.Many2many('library.tag', string='Tags')  # Tags associated with the category
