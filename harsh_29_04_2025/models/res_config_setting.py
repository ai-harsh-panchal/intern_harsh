# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderConfigSettings(models.TransientModel):
    """
    Inherit res config setting for configure multiple approval thresholds
    by sales manager to sale order
    """
    _inherit = 'res.config.settings'

    sales_manager_ids = fields.Many2many(
        'res.users',
        string="Sales Manager",
    )

    def set_values(self):
        res = self.env['ir.config_parameter'].sudo().set_param('harsh_29_04_2025.sales_manager_ids')
        return res
