# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    """
    This model is inherit for add new field and customize the form view of product template
    """
    _inherit = 'product.template'

    is_library_book = fields.Boolean(string='Is Library Book', default=False)
    author = fields.Char(string='Author Name')
    publisher = fields.Char(string='Publisher Name')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Number of Pages')
    available = fields.Boolean(string='Available in Stock', default=True)
    barcode = fields.Char(string='ISBN Number', required=True)
    status = fields.Selection([('available', 'Available'),
                               ('borrowed', 'Borrowed'),
                               ('reserved', 'Reserved')],
                              string='Status')

    def action_borrow(self):
        """
        this function is used to set the status borrowed
        """
        self.status = 'borrowed'
        self.available = False

    def action_available(self):
        """
        this function is used to set the status back to available from borrowed
        """
        self.status = 'available'
        self.available = True
