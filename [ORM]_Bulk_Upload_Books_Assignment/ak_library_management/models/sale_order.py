# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """
    i have inherit sale order for perform approval task
    """
    _inherit = 'sale.order'

    approval_required = fields.Boolean(string="Approval Required")
    approved_confirm = fields.Boolean(string="Approved confirm")

    def action_confirm(self):
        """
        this method check that if approved _confirm is not true then open the validation
        popup otherwise sale order confirm
        """
        if self.approved_confirm:
            return super(SaleOrder, self).action_confirm()
        else:
            for line in self.order_line:
                product = line.product_id
                on_hand_quantity = product.qty_available
                if on_hand_quantity < 5:
                    self.approval_required = True
                    return {
                        'name': 'Approval Required',
                        'type': 'ir.actions.act_window',
                        'res_model': 'sale.order.wizard',
                        'view_mode': 'form',
                        'view_type': 'form',
                        'target': 'new',
                        'context': {
                            'default_message': "Approval is required to proceed with this order due to stock is less then 5."
                        }
                    }

            return super(SaleOrder, self).action_confirm()

    def action_approve(self):
        """
        this function approve the sale order record
        """
        if not self.env.user.is_manager:
            raise UserError("You are not manager to approve this order.")
        self.approval_required = False
        self.approved_confirm = True
        self.state = 'draft'

    def action_reject(self):
        """
        this function reject the sale order record
        """
        self.state = 'cancel'
        self.approval_required = False
