# -*- coding: utf-8 -*-

from odoo import models, fields,api
from datetime import timedelta
from odoo.models import ValidationError


class BorrowTransactionHistory(models.Model):
    """
    Manages and tracks library book borrowing transactions.
    This model maintains detailed records of book borrowing activities including
    customer information, borrowed books, transaction dates, and deposit details.
    """
    _name = 'borrow.transaction.history'
    _description = 'Borrow Transaction History'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one('res.partner', string='Customer')
    books_ids = fields.Many2many('product.template', string='Books', domain=[('is_library_book', '=', 'True')])
    borrow_start_date = fields.Date(string='Borrow Start Date', default=fields.datetime.now())
    borrow_end_date = fields.Date(string='Borrow End Date', required=True)
    deposit_amount = fields.Float(string='Deposit Amount')
    is_member = fields.Boolean(string="is_member", related='customer_id.is_member')
    non_trust_worthy = fields.Boolean('res.partner', related="customer_id.is_member")

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def validate_borrow_dates(self):
        """
        Validates that the borrow end date is after the start date.
        Raises ValidationError if end date precedes start date.
        param: self
        Raises:
            ValidationError: When borrow end date is earlier than start date
        """
        for record in self:
            if record.borrow_start_date > record.borrow_end_date:
                raise ValidationError('Borrow end date not less then the start date')

    def _get_wizard_popup(self, title, message):
        """
        this function is used for display the wizard popup message
        parameter: self
        return: Dictionary action open form view
        return type: dict
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
        parameter: self
        return: _get_wizard_popup method
        return type: dict
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


        # If the customer is trying to borrow 5 or more books
        if len(self.books_ids) >= 5:
            search_recd = self.search([('customer_id.id', "=", self.customer_id.id)])
            books_name = []
            [books_name.append(book.name) for rec in search_recd[:-1]
             for book in rec.books_ids if book.name not in books_name]

            if books_name:
                return self._get_wizard_popup(title='warning',
                            message=f"Customer already has [{len(search_recd) - 1}] open borrow transactions "
                           f"with {books_name} books. "
                           f"Are you sure you want to borrow more books?")

            return self._get_wizard_popup(title='warning',
                        message="Are you sure you want to allow "
                       "borrowing more than 5 books for this customer?")

        # decrease a stock of product when borrowed
        for rec in self.book_ids:
            if rec.qty_available:
                product_id = self.env['product.product'].search([('name', '=', rec.name)])
                loc = self.env['stock.quant'].search([('product_id.name', '=', rec.name)])
                self.env['stock.quant']._update_available_quantity(product_id, loc[0].location_id, quantity=-1)


    def notify_due_returns(self):
            """
            This method checks for records with a borrow_end_date that is 2 days from today
            and sends notifications to the respective customers.
            param : self
            return: None
            """
            all_recd = self.search([])
            for record in all_recd:
                for rec in record.books_ids:
                    if rec.status == 'borrowed':
                        date_deadline = record.borrow_start_date + timedelta(days=2)
                        if record.borrow_end_date == date_deadline:
                            self.env['bus.bus']._sendone(record.customer_id, 'simple_notification', {
                                'type': 'warning',
                                'message': f"reminder: your book return date is {record.borrow_end_date}",
                            })

    def action_return_books(self):
        """
        Marks selected books as returned in the library system.

        Updates the status of borrowed books to 'return' when customers
        physically return them to the library.

        param: self
        Returns: None
        """
        for rec in self.books_ids:
            if rec.status == 'borrowed':
                rec.status = 'return'
                self.env['bus.bus']._sendone(self.customer_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"Book '{rec.name}' has been returned successfully.",
                })

    @api.constrains('customer_id', 'books_ids')
    def _check_overdue_books(self):
        """
        Prevents customers from borrowing new books if they have overdue books.
        Checks during creation of new borrow transactions.
        param : self
        Returns: None
        """
        for record in self:
            if record.customer_id and record.books_ids:
                overdue_count = self.env['borrow.transaction.history'].search_count([
                    ('customer_id', '=', record.customer_id.id),
                    ('borrow_end_date', '<', fields.Date.today()),
                    ('books_ids.status', '=', 'borrowed'),
                ])

                if overdue_count:
                    raise ValidationError(
                        f"Customers with overdue books cannot borrow new ones until they return the overdue items."
                    )
