# -*- coding: utf-8 -*-
from odoo import models, fields
class Member(models.Model):
    """
    Model representing a Member details in the library.
    """
    _name = 'library.member'
    _description = 'Library Member Model'

    name = fields.Char(string='Member Name', required=True)# name of member
    email = fields.Char(string='Email ID')# email of member
    phone = fields.Char(string='Contact Number')# phone number of member
    membership_date = fields.Date(string='Membership Start Date')# membership date of member
    book_id = fields.Many2one('library.book', string='Book Allocate')# show that book borrowed by member
