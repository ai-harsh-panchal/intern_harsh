# -*- coding: utf-8 -*-

from odoo import models, fields

class Member(models.Model):
    """
    Model representing a Member details in the library.
    """
    _name = 'library.member'
    _description = 'Library Member Model'

    name = fields.Char(string='Member Name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
    book_id = fields.Many2one('library.book', string='Book Allocate')
