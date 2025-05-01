# -*- coding: utf-8 -*-

from odoo import models, fields


class SalesManagerApproval(models.Model):
    """
    This model is manage the approval workflow of sale order by manager
    - Tracks if approval is required for the sale order
    - Manages approval the sale order
    """

    _name = 'sales.manager.approval'
    _description = 'Sales Manager Approval Threshold'
    _sql_constraints = [
        ('unique_threshold', 'UNIQUE(approval_threshold)', 'Threshold amount is already configured.')
    ]

    user_id = fields.Many2one('res.users', string='Sales Manager', required=True)
    approval_threshold = fields.Float(string='Approval Threshold Amount', required=True)


