# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BorrowBooksWizard(models.Model):
    _name = 'borrow.books.wizard'
    _description = 'Wizard for Borrowing Books'

    message = fields.Text(string="Wizard Message", readonly=True)
