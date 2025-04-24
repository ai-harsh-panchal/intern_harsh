# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import models, fields, api
from datetime import datetime,date
from odoo.models import ValidationError


class BorrowTransactionHistory(models.Model):
    """
    Manages and tracks library book borrowing transactions.
    This model maintains detailed records of book borrowing activities including
    customer information, borrowed books, transaction dates, and deposit details.
    """

    _name = "borrow.transaction.history"
    _description = "Borrow Transaction History"
    _rec_name = "customer_id"

    customer_id = fields.Many2one(
        comodel_name="res.partner", string="Customer", required=True
    )
    books_ids = fields.Many2many(
        comodel_name="product.template",
        string="Books",
        domain=[("is_library_book", "=", "True")],
    )
    borrow_start_date = fields.Date(
        string="Borrow Start Date", default=fields.datetime.now()
    )
    borrow_end_date = fields.Date(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")
    is_member = fields.Boolean(related="customer_id.is_member")
    is_active = fields.Boolean(compute='_compute_active_transaction', store=True)
    limit_exceeded = fields.Boolean(compute='_compute_limit_exceeded', store=True)

    @api.depends('books_ids')
    def _compute_limit_exceeded(self):
        """
        this function checks the limit of borrowing books
        param: self
        return: None
        """
        for transaction_limit in self:
            limit = self.env['ir.config_parameter'].sudo().get_param('ak_library_management.borrowing_limit')
            transaction_limit.limit_exceeded = len(transaction_limit.books_ids) > int(limit)

    @api.depends('borrow_end_date')
    def _compute_active_transaction(self):
        """
        check the transaction is active or not and set true or false in boolean field
        param: self
        return: None
        """
        for active_transaction in self.search([]):
            active_transaction.is_active = active_transaction.borrow_end_date >= date.today()

    @api.constrains("borrow_start_date", "borrow_end_date")
    def validate_borrow_dates(self):
        """
        Validates that the borrow end date is after the start date.
        Raises ValidationError if end date precedes start date.
        param: self
        Raises:
            ValidationError: When borrow end date is earlier than start date
        """
        if self.filtered(lambda r: r.borrow_start_date > r.borrow_end_date):
            raise ValidationError("Borrow end date not less then the start date")
        if self.filtered(lambda r: r.deposit_amount <= 0 and not r.is_member):
            raise ValidationError("Deposit Amount must be greater than zero")

    def show_warning_wizard(self, message, next_action=None):
        """
        Helper function to return a warning wizard action.
        This function is now defined as a separate method to improve code structure.
        param: message,self,next_action
        Returns: dict: A dictionary representing an action to display a warning wizard.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warning',
            'res_model': 'borrow.books.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_borrow_wizard_id': self.id,
                'default_message': message,
                'default_next_action': repr(next_action) if next_action else None,
            }
        }

    def action_confirm(self):
        """
        this function is used to confirm the borrow transaction with multiple checks
        param: self
        return: recordset
        """
        warnings = []

        # **Check 1: Customer Trustworthiness**
        if self.customer_id.not_trust_worthy:
            warnings.append("Customer is not trustworthy. Are you sure you want to continue?")

        # **Check 2: Product Availability (books out of stock)**
        out_of_stock_books = self.books_ids.filtered(lambda book: book.qty_available <= 0)
        if out_of_stock_books:
            book_names = ", ".join(out_of_stock_books.mapped('name'))  # Get book names
            warnings.append(f"The following books are out of stock: {book_names}.")

        # **Check 3: Borrowing More Than 5 Books**
        if len(self.books_ids) >= 5:
            search_recd = self.search([('customer_id.id', "=", self.customer_id.id)], order='id desc', offset=1)
            books_name = {book.name for rec in search_recd for book in rec.books_ids}
            if books_name:
                warnings.append(f"Customer already has [{len(search_recd)}] open borrow transactions with "
                                f"{', '.join(books_name)} books. Are you sure you want to borrow more books?")
            else:
                warnings.append("Are you sure you want to allow borrowing more than 5 books for this customer?")

        if warnings:
            return self.show_warning_wizard(warnings[0], next_action=warnings[1:] if len(warnings) > 1 else None)
        else:
            return self._process_borrow_transaction()

    def _process_borrow_transaction(self):
        """
        Finalizes the borrow transaction and updates stock quantities.
        param: self
        returns: True
        """
        for transaction_data in self.books_ids:
            loca = self.env['stock.quant'].search([('product_tmpl_id.id', '=', transaction_data.id)], limit=1)
            if loca:
                new_qty = -1 if transaction_data.qty_available <= 0 else -1
                self.env['stock.quant']._update_available_quantity(loca.product_id, loca.location_id, quantity=new_qty)
        return True

    def _cron_notify_due_returns(self):
        """
        This method checks for records with a borrow_end_date that is 2 days from today
        and sends notifications to the respective customers and send a email message
        param : self
        return: None
        """

        due_date = date.today() + timedelta(days=2)
        borrowed_records = self.search([
            ('borrow_end_date', '=', due_date),
            ('books_ids.status', '=', 'borrowed')
        ])
        mail_template = self.env.ref("ak_library_management.email_template_library_return_reminder")
        for transaction in borrowed_records:
            mail_template.send_mail(transaction.id, force_send=True)
            self.env["bus.bus"]._sendone(
                transaction.customer_id,
                "simple_notification",
                {
                    "type": "warning",
                    "message": f"reminder: your book return date is {transaction.borrow_end_date}",
                },
            )

    def action_return_books(self):
        """
        Marks selected books as returned in the library system.

        Updates the status of borrowed books to 'return' when customers
        physically return them to the library.
        param: self
        Returns: None
        """
        borrowed_books = self.books_ids.filtered(lambda books: books.status == "borrowed")
        borrowed_books.write({'status': 'return'})

        for book in borrowed_books:
            self.env["bus.bus"]._sendone(
                self.customer_id,
                "simple_notification",
                {
                    "type": "success",
                    "message": f"Book '{book.name}' has been returned successfully.",
                },
            )

    @api.constrains("customer_id", "books_ids")
    def _check_overdue_books(self):
        """
        Prevents customers from borrowing new books if they have overdue books.
        Checks during creation of new borrow transactions.
        param : self
        Returns: None
        """
        customer_record = self.filtered(lambda b: b.customer_id and b.books_ids)
        overdue_count = self.env["borrow.transaction.history"].search_count(
            [
                ("customer_id", "=", customer_record.customer_id.id),
                ("borrow_end_date", "<", fields.Date.today()),
                ("books_ids.status", "=", "borrowed"),
            ]
        )

        if overdue_count:
            raise ValidationError(
                f"Customers with overdue books cannot borrow new ones until they return the overdue items."
            )

    def _cron_send_overdue_notices(self):
        """
        Send overdue notices to customers with overdue books
        This method is called weekly by the scheduled action
        param : self
        return: None
        """
        overdue_records = self.search(
            [
                ("borrow_end_date", "<", fields.Date.today()),
                ("books_ids.status", "=", "borrowed"),
            ]
        )

        template = self.env.ref("ak_library_management.email_template_library_overdue")
        for borrow_transaction in overdue_records:
            template.send_mail(borrow_transaction.id, force_send=True)
