# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    """
    inherit project_project model for job name functionality
    """
    _inherit = 'project.project'

    job_name = fields.Char(string='Job Name')
    is_job_name = fields.Boolean(compute="_compute_job_name", store=True)
    sale_order_id = fields.Many2one('sale.order')

    @api.depends('job_name')
    def _compute_job_name(self):
        """
        this function is used to set the status of is_job_name
        """
        for record in self:
            record.is_job_name = bool(record.sale_order_id and record.job_name)
