# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    Extends sale.order model to implement approval workflow functionality.
    This class adds approval management features to sales orders:
    - Tracks if approval is required for the sale order
    - Manages approval confirmation status
    """
    _inherit = 'sale.order'

    approval_required = fields.Boolean(string="Approval Required")
    approved_confirm = fields.Boolean(string="Approved Confirm")

    def action_confirm(self):
        """
        Checks stock levels and requires approval for products with low quantity.
        Opens approval wizard if needed, otherwise confirms sale order.
        parameter: self
        return: Call base action_confirm method
        """
        for order in self:
            if not order.approved_confirm and any(line.product_id.qty_available < 5 for line in order.order_line):
                order.approval_required = True

                low_stock_products = [
                    line.product_template_id.name
                    for line in order.order_line
                    if line.product_id.qty_available < 5
                ]
                return {
                    'name': 'Approval Required',
                    'type': 'ir.actions.act_window',
                    'res_model': 'sale.order.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_message': f"Approval required for {', '.join(low_stock_products)} product due to stock being less than 5."
                    }
                }
        return super().action_confirm()

    def action_approve(self):
        """
        Approves multiple sale orders if user has manager rights.
        Updates approval status and state for all selected orders.
        parameter: self
        return: None
        """
        if not self.env.user.is_manager:
            raise ValidationError("You are not a manager to approve these orders.")

        self.write({
            'approval_required': False,
            'approved_confirm': True,
            'state': 'draft'
        })

    def action_reject(self):
        """
        Rejects multiple sale orders and cancels them.
        parameter: self
        return: call base action_cancel method
        """
        self.write({'approval_required': False})
        return self.action_cancel()
