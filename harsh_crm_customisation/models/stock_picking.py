# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    """
    inherit stock picking model for job name functionality
    """
    _inherit = 'stock.picking'

    job_name = fields.Char(string='Job Name')
