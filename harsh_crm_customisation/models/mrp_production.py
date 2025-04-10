# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    """
    inherit mrp_production model for job name functionality in manufactured record
    """
    _inherit = 'mrp.production'

    job_name = fields.Char(string='Job Name')

