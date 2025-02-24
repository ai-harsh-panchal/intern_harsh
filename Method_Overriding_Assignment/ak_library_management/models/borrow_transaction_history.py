# -*- coding: utf-8 -*-

from odoo import models, fields,api
from datetime import datetime
from odoo.models import ValidationError


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
    non_trust_worthy = fields.Boolean(related="customer_id.is_member")

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def check_dates(self):
        for record in self:
            if record.borrow_start_date > record.borrow_end_date:
                raise ValidationError('end date must be less than start date')


    def action_borrow_books(self):
        for book in self.books_ids:
            if book.qty_available == 0:
                return {
                    'name': 'Book Out of Stock',
                    'type': 'ir.actions.act_window',
                    'res_model': 'borrow.books.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_message': f"The book '{book.name}' is out of stock. Do you want to proceed?"},
                }
            active_transactions = self.env['borrow.transaction.history'].search_count([
                ('customer_id', '=', self.customer_id.id),
                ('borrow_end_date', '>=', fields.Date.today()),  # Active transactions with future end date
            ])

            if active_transactions > 0:
                # Find how many books are already borrowed in active transactions
                borrowed_books = sum(self.env['borrow.transaction.history'].search([
                    ('customer_id', '=', self.customer_id.id),
                    ('borrow_end_date', '>=', fields.Date.today()),
                ]).mapped('books_ids.qty_available'))

                return {
                    'name': 'Customer Already Borrowed Books',
                    'type': 'ir.actions.act_window',
                    'res_model': 'borrow.books.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_message': f"you already has active - {borrowed_books}  borrowed books Are you sure you want to borrow more books?"

                    },
                }

        if self.customer_id.not_trust_worthy:
            return {
                'name': 'Customer Not Trustworthy',
                'type': 'ir.actions.act_window',
                'res_model': 'borrow.books.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_message': " Are you sure you want to continue?"},
            }
        else:
            borrowing_record = self.create({
                'customer_id': self.customer_id.id,
                'borrow_start_date': self.borrow_start_date,
                'borrow_end_date': self.borrow_end_date,
                'books_ids': self.books_ids,
                'deposit_amount': self.deposit_amount,
            })

            for book in self.books_ids:
                book.qty_available -= 1
            return True
