# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Member(models.Model):
    _name = 'library.member'
    _description = 'Library Member Model'

    name = fields.Char(string='Member Name', required=True)
    email = fields.Char(string='Email ID')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
    book_id = fields.Many2many('library.book', string='Books')
