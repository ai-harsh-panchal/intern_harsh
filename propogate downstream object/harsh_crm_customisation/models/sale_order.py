# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    """
    Inherits from the sale.order model to extend its functionality.
    This model adds a job_name field and overrides the action_confirm method
    to set the job_name based on the sale order's origin. It also updates
    related picking records, manufacturing orders, and projects record
    """
    _inherit = 'sale.order'

    opportunity_id = fields.Many2one('crm.lead')
    job_name = fields.Char(string='Job Name', compute="_compute_job_from_opportunity", store="True")

    @api.depends('opportunity_id')
    def _compute_job_from_opportunity(self):
        """
        If opportunity id is change than job name is change this method are
        depends on crm name

        param: None
        return: None
        """
        for rec in self:
            if rec.opportunity_id:
                rec.job_name = rec.opportunity_id.name

    def action_confirm(self):
        """
            Confirm the sale order and perform additional actions.

            This method overrides the default action_confirm method to:
            - Set the job_name of the sale order from its origin if available.
            - Update the job_name in related stock pickings.
            - Update the job_name in related manufacturing orders.
            - Update the name and job_name in related projects.

            param : self
            return : recordset
        """
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.origin:
                order.job_name = order.origin

            for picking in order.picking_ids:
                picking.job_name = order.job_name

            mfg_orders = self.env['mrp.production'].search([('origin', '=', order.name)])
            for mo in mfg_orders:
                mo.job_name = order.job_name

            for project in order.project_ids:
                project.name = f"{order.name} - {order.job_name}"
                project.job_name = order.job_name
        return res

    def _prepare_invoice(self):
        """
        Inherit prepare invoice function and pass the job name field data to invoice

        param: None
        return: dictionary
        """
        res = super(SaleOrder, self)._prepare_invoice()
        res["job_name"] = self.job_name
        return res
