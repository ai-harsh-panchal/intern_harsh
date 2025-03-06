# -*- coding: utf-8 -*-

from odoo import models, fields


class Tag(models.Model):
    """
    Model representing a tag that can be associated with books.
    """
    _name = 'library.tag'
    _description = 'Library Tag'

    name = fields.Char(string='Tag Name', required=True)
    description = fields.Text(string='Tag Description')
