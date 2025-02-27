# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderWizard(models.TransientModel):
    """
    this model is used for only wizard popup message
    """
    _name = 'sale.order.wizard'
    _description = 'sale order wizard popup'

    message = fields.Text(string="Message", readonly=True)
