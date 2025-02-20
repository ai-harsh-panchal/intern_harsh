# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    """
    i have inherit the model and  add a boolean field name is_manager
    """
    _inherit = 'res.users'

    is_manager = fields.Boolean(string='Is Manager')