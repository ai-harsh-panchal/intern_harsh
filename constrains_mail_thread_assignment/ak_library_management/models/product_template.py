# -*- coding: utf-8 -*-
from pyasn1_modules.rfc5280 import anotherNameMap

from odoo import models, fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta


class ProductTemplate(models.Model):
    """
    This model is inherit for add new field and customize the form view of product template
    """
    _inherit = 'product.template'

    is_library_book = fields.Boolean(string='Is Library Book')
    author = fields.Char(string='Author Name')
    publisher = fields.Char(string='Publisher Name')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Number of Pages')
    available = fields.Boolean(string='Available in Stock')
    status = fields.Selection([('available', 'Available'),
                               ('borrowed', 'Borrowed'),
                               ('unavailable', 'Unavailable'),
                               ('return', 'Return')],
                              string='Status',
                              tracking=True,
                              default='available')

    @api.constrains('unavailable')
    def action_borrow(self):
        """
        This function is an action to set the status to 'borrowed' and mark the book as unavailable.
        It validates that the book is not 'unavailable' before proceeding.
        parameter: self
        return: None
        """
        for record in self:
            if record.status == 'unavailable':
                raise ValidationError("The book is marked as 'Unavailable' and cannot be borrowed.")
            record.status = 'borrowed'
            record.available = False
            record.message_post(
                body=f"The book was borrowed by {self.env.user.name} on {fields.Datetime.now()}",
                subject="Book Borrowed"
            )
            # Schedule an activity with a due date for the borrower
            due_date = fields.Date.today() + timedelta(days=10)
            record.activity_schedule(
                summary=f"Borrower: {self.env.user.name}, Deadline: {due_date}",
                user_id=self.env.user.id,
                date_deadline=due_date,
            )

    def action_available(self):
        """
        This function is used to set the status back to available from borrowed.
        parameter: self
        return: None
        """
        self.status = 'available'
        self.available = True


    def action_return(self):
        """
        This function marks the book as returned, updates the status to 'return',
        and creates a log note (not a chatter notification).
        parameter: self
        return: None
        """
        for record in self:
            record.status = 'return'
            # Create a custom log note
            record.message_post(
                body=f"The book was returned and is now available in stock",
                subject="Book Returned",
                message_type="comment"
            )


    @api.depends('author')
    def _compute_display_name(self):
        """
        this function is used for display name in dropdown particular format
        parameter: self
        return: None
        """
        for record in self:
            author_name = record.author if record.author else "Unknown Author"
            record.display_name = f"{author_name}-{record.name}"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=None):
        """
        override name_search method to search book by author name.
        param: name, args, operator, limit
        parameter: self
        return: Base name search method
        return type: List of tuple
        """
        args = list(args or [])
        if name:
            args += [('author', operator, name)]
        return super().name_search(args=args, limit=limit)


    @api.model_create_multi
    def create(self,vals_list):
        """
        this function is used for create a unique sequence in refernce field of product
        parameter: self
        return: Base create orm method
        return type: recordset
        """
        for vals in vals_list:
            vals['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        return super(ProductTemplate, self).create(vals_list)


    def borrowed_books(self):
        """
        this function open the borrow transaction wizard model form view
        parameter: self
        return: dictionary of action open form
        return type: dict
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrowed Books',
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

    @api.constrains('status')
    def action_update_status(self):
        """
        This method sends a notification to the user whenever the status of the book is updated.
        parameter: self
        return: None
        """
        for record in self:
            message = f"The status of the book '{record.name}' has been updated to '{record.status}'."
            self.env['bus.bus']._sendone(
                self.env.user.partner_id,
                'simple_notification',
                {'title': 'Library Update', 'message': message, 'type': 'success', 'sticky': True}
            )
