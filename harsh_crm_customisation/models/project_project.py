# -*- coding: utf-8 -*-

from odoo import models, fields


class ProjectProject(models.Model):
    """
    inherit project_project model for job name functionality
    """
    _inherit = 'project.project'

    job_name = fields.Char(string='Job Name')
