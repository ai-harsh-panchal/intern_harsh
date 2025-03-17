# -*- coding: utf-8 -*-#

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    library_book_limit = fields.Integer(
        string='Borrowing Limit'
    )
