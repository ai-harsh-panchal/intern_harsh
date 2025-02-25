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
        # condition check that new customer try to borrow the book
        new = self.search_count([('customer_id', '=', self.customer_id.id)])
        if new <= 1:
            return self._get_wizard_popup(
                title='New Customer',
                message="Are you sure you want to allow borrowing more than 5 books for this customer?"
            )

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

        # condition check the borrow transaction of particular customer if more then 0 then show popup msg
        customer_transactions = self.env['borrow.transaction.history'].search(
            [('customer_id', '=', self.customer_id.id)])
        total_borrowed_books = sum(len(transaction.books_ids) for transaction in customer_transactions)
        if total_borrowed_books > 0:
            borrowed_book_names = ', '.join(
                book.name for transaction in customer_transactions for book in transaction.books_ids
            )
            return self._get_wizard_popup(
                title='Total Borrowed Books',
                message=f"This customer has borrowed a total of {total_borrowed_books} books: {borrowed_book_names}. Are you sure you want them to borrow more?"
            )

        # create record
        borrowing_record = self.create({
            'customer_id': self.customer_id.id,
            'borrow_start_date': self.borrow_start_date,
            'borrow_end_date': self.borrow_end_date,
            'books_ids': [(6, 0, self.books_ids.ids)],
            'deposit_amount': self.deposit_amount,
        })
