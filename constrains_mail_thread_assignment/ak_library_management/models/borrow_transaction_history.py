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
        """
        this function check that end date is not less then start date
        """
        for record in self:
            if record.borrow_start_date > record.borrow_end_date:
                raise ValidationError('end date must be less than start date')

    def _get_wizard_popup(self, title, message):
        """
        this function is used for display the wizard popup message
        """
        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'res_model': 'borrow.books.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_message': message
            },
        }

    def action_borrow_books(self):
        """
        this function create the record & check the all condition as per given
        """
        # Condition: Customer is not trustworthy
        if self.customer_id.not_trust_worthy:
            return self._get_wizard_popup(
                title='Customer Not Trustworthy',
                message="The customer is marked as not trustworthy. Are you sure you want to continue?"
            )

        # Condition: Books are out of stock
        out_of_stock_books = self.books_ids.filtered(lambda book: book.qty_available == 0)
        if out_of_stock_books:
            return self._get_wizard_popup(
                title='Book Out of Stock',
                message=f"The book '{out_of_stock_books[0].name}' is out of stock. Do you want to proceed?"
            )

        if len(self.books_ids) >= 5:
            # Check for existing open borrow transactions
            open_borrow_transactions = self.env['borrow.transaction.history'].search([
                ('customer_id', '=', self.customer_id.id),
            ])

            if open_borrow_transactions:
                # Case A: Existing customer with open borrow transactions
                open_books_count = sum(len(transaction.books_ids) for transaction in open_borrow_transactions)
                return self._get_wizard_popup(
                    title='Warning',
                    message=f"Customer already has {len(open_borrow_transactions)} open borrow transactions with {open_books_count} books. Are you sure you want to borrow more books?"
                )
            else:
            # Case C: New or existing customer borrowing fewer than 5 books
                return self._get_wizard_popup(
                    title='Information',
                    message="Borrowing fewer than 5 books is allowed. Do you want to borrow these books?"
                )

        # case c Decrease Stock for Each Book in the Borrow Process
        for rec in self.books_ids:
            if rec.qty_available:
                rec.qty_available -= 1
