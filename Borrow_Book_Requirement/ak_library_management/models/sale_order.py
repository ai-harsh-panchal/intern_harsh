# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    i have inherit sale order for perform approval task
    """
    _inherit = 'sale.order'

    approval_required = fields.Boolean(string="Approval Required")
    approved_confirm = fields.Boolean(string="Approved Confirm")

    def action_confirm(self):
        """
        this method check that if approved _confirm is not true then open the validation
        popup otherwise sale order confirm
        """
        if not self.approved_confirm and any(line.product_id.qty_available < 5 for line in self.order_line):
            self.approval_required = True
            return {
                'name': 'Approval Required',
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_message': "Approval is required to proceed with this order due to stock being less than 5."
                    }
                }
        return super(SaleOrder, self).action_confirm()

    def action_approve(self):
        """
        this function approve the sale order record
        """
        if not self.env.user.is_manager:
            raise ValidationError("You are not manager to approve this order.")
        self.approval_required = False
        self.approved_confirm = True
        self.state = 'draft'

    def action_reject(self):
        """
        This function rejects the sale order record and cancel using
        base cancel method
        """
        self.approval_required = False
        return self.action_cancel()
