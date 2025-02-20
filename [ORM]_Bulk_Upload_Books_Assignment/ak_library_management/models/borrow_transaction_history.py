# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime


class BorrowTransactionHistory(models.Model):
    """
    this model is show the details about customer borrow transaction history
    """
    _name = 'borrow.transaction.history'
    _description = 'Borrow Transaction History'

    customer_id = fields.Many2one('res.partner', string='Customer')
    books_ids = fields.Many2many('product.template', string='Books', domain=[('is_library_book', '=', 'True')])
    borrow_start_date = fields.Datetime(string='Borrow Start Date', default=datetime.today())
    borrow_end_date = fields.Datetime(string='Borrow End Date', required=True)
    deposit_amount = fields.Float(string='Deposit Amount')
    is_member = fields.Boolean(string="is_member", related='customer_id.is_member')
