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
    # barcode = fields.Char(string='ISBN Number', required=True)
    status = fields.Selection([('available', 'Available'),
                               ('borrowed', 'Borrowed'),
                               ('reserved', 'Reserved')],
                              string='Status', default='available')

    def action_borrow(self):
        """
        this function is used to set the status borrowed
        when book is available or status is available then we can borrowed the book
        """
        for record in self:
            if record.available and record.status == 'available':
                record.status = 'borrowed'
                record.available = False
            else:
                return record.status == 'reserved'

    def action_available(self):
        """
        this function is used to set the status back to available from borrowed
        """
        for record in self:
            if record.status == 'borrowed':
                record.status = 'available'
                record.available = True
            else:
                pass
