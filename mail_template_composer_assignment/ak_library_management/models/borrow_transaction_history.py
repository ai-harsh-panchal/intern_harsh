# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import models, fields, api
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

    def _get_wizard_popup(self, title, message):
        """
        this function is used for display the wizard popup message
        parameter: self, title, message
        return: Dictionary action open form view
        return type: dict
        """
        return {
            "name": title,
            "type": "ir.actions.act_window",
            "res_model": "borrow.books.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_message": message},
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
                title="Customer Not Trustworthy",
                message="The customer is marked as not trustworthy. Are you sure you want to continue?",
            )


        # Condition: Books are out of stock
        out_of_stock_books = self.books_ids.filtered(
            lambda book: book.qty_available == 0
        )
        if out_of_stock_books:
            book_names = ", ".join(out_of_stock_books.mapped("name"))
            message = f"The following books are out of stock: {book_names}. Do you want to proceed?"
            return self._get_wizard_popup(title="Book Out of Stock", message=message)

        # decrease a stock of product when borrowed
        for rec in self.books_ids.filtered(lambda book: book.qty_available):
            loc = self.env['stock.quant'].search([('product_tmpl_id.id', '=', rec.id)], limit=1)
            self.env['stock.quant']._update_available_quantity(loc.product_id, loc.location_id,
                                                                    quantity=-1)


        # If the customer is trying to borrow 5 or more books
        if len(self.books_ids) >= 5:
            books_record = self.search(
                [("customer_id.id", "=", self.customer_id.id)],
                order="id desc",
                offset=1,
            )
            books_name = []
            books_name = books_record.mapped('books_ids').filtered(lambda b: b.name not in books_name).mapped(
                'name')

            if books_name:
                return self._get_wizard_popup(
                    title="warning",
                    message=f"Customer already has [{len(books_record)}] open borrow transactions "
                            f"with {books_name} books. "
                            f"Are you sure you want to borrow more books?",
                )

            return self._get_wizard_popup(
                title="warning",
                message="Are you sure you want to allow "
                        "borrowing more than 5 books for this customer?",
            )

    def _cron_notify_due_returns(self):
        """
        This method checks for records with a borrow_end_date that is 2 days from today
        and sends notifications to the respective customers and send a email message
        param : self
        return: None
        """
        borrowed_records = self.search([]).filtered(
            lambda r: any(book.status == "borrowed" for book in r.books_ids)
                      and r.borrow_end_date == r.borrow_start_date + timedelta(days=2)
        )
        mail_template = self.env.ref("ak_library_management.email_template_library_return_reminder")
        for record in borrowed_records:
            mail_template.send_mail(record.id, force_send=True)
            self.env["bus.bus"]._sendone(
                record.customer_id,
                "simple_notification",
                {
                    "type": "warning",
                    "message": f"reminder: your book return date is {record.borrow_end_date}",
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
        for record in overdue_records:
            template.send_mail(record.id, force_send=True)
