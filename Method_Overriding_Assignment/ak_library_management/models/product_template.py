# -*- coding: utf-8 -*-

from odoo import models, fields,api


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
                               ('reserved', 'Reserved')],
                              string='Status',
                              default='')

    @api.depends('author')
    def _compute_display_name(self):
        for record in self:
            author_name = record.author if record.author else "Unknown Author"
            record.display_name = f"{author_name}-{record.name}"

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

    @api.model_create_multi
    def create(self,vals_list):
        """
        this function is used for create a unique sequence in refernce field of product
        """
        for vals in vals_list:
            vals['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        return super(ProductTemplate, self).create(vals_list)

    def borrowed_books(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrowed Books',
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
