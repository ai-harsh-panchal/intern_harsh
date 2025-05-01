# -*- coding: utf-8 -*-

from odoo import models, api, fields


class SaleOrder(models.Model):
    """
    Inherit Sale order model to manage Sales Order validation.
    On creation or update, the system checks the appropriate threshold.
    """

    _inherit = 'sale.order'

    approval_required = fields.Boolean(default=False)
    state = fields.Selection(selection_add=[
        ('pending_approval', 'Pending Approval')
    ])
    approved_by = fields.Many2one('res.users', string='Approved By', tracking=True)
    approved_date = fields.Datetime(string='Approved Date', tracking=True)

    @api.model_create_multi
    def create(self, vals):
        """
        This function manages the approval process at sale order creation.
        param : vals
        return : recordset
        """
        threshold_records = self.env['sales.manager.approval'].search([])
        orders = super(SaleOrder, self).create(vals)
        for order in orders:
            for record in threshold_records:
                if order.amount_total > record.approval_threshold:
                    order.approval_required = True
                    order.state = 'pending_approval'
                    order.message_post(
                        body=f"Approval Request for amount total {order.amount_total} and Assigned to {threshold_records.user_id.name} Approver",
                        subject="Approval Request",
                        message_type="comment"
                    )
                    break
        return orders

    def write(self, vals):
        """
        This function manages the approval process at sale order update.
        param : vals
        return : bool
        """
        result = super(SaleOrder, self).write(vals)

        for order in self:
            threshold_records = self.env['sales.manager.approval'].search([])
            if 'amount_total' in vals or 'order_line' in vals:
                if order.amount_total > max(record.approval_threshold for record in threshold_records):
                    order.approval_required = True
                    order.state = 'pending_approval'
                    order.message_post(
                        body=f"Approval Request for amount total {order.amount_total} and Assigned to {threshold_records.user_id.name} Approver",
                        subject="Approval Request",
                        message_type="comment"
                    )
        return result

    def send_for_approval(self):
        """
        Send an email to the manager for approval request.
        param : self
        return : None
        """
        template = self.env.ref('harsh_29_04_2025.email_template_sale_approval_request')
        if template:
            for order in self:
                template.send_mail(order.partner_id.id, force_send=True)

    def approve_order(self):
        """
        this function approves the sale order which exceed the
        threshold amount
        param : None
        """
        self.write({
            'approval_required': False,
            'state': 'draft',
            'approved_by': self.env.user,
            'approved_date': fields.datetime.now()
        })


    @api.model
    def _cron_reminder_approvals(self):
        """
        This function is used for cron to send email automatically
        to sales managers for approval requests based on sale order amount total.
        param : none
        return: recordset
        """
        sale_orders = self.env['sale.order'].search([
            ('approval_required', '=', True),
            ('state', '=', 'pending_approval')
        ])
        threshold_records = self.env['sales.manager.approval'].search([])
        manager_orders = {}
        for order in sale_orders:
            for record in threshold_records:
                if order.amount_total > record.approval_threshold:
                    if record.user_id.id not in manager_orders:
                        manager_orders[record.user_id.id] = []
                    manager_orders[record.user_id.id].append(order)
        template = self.env.ref('harsh_29_04_2025.email_template_sale_approval_request')
        for manager_id, orders in manager_orders.items():
            if template:
                order_list = ', '.join(order.name for order in orders)
                email_body = f"You have the following sale orders pending approval: {order_list}."
                template.body_html = email_body
                template.send_mail(manager_id, force_send=True)
