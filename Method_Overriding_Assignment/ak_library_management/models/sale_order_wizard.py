# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.wizard'
    _description = 'sale order wizard popup'

    message = fields.Text(string="Message", readonly=True)
