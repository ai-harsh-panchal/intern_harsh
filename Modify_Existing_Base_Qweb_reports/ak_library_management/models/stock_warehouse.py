#-*- coding: utf-8 -*-#

from odoo import models, fields,api
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    library_assistant_id = fields.Many2one(comodel_name='hr.employee', string='Library Assistant')
    worker_id = fields.Many2many(comodel_name='hr.employee', string='Worker')

    @api.constrains('library_assistant_id', 'worker_id')
    def _check_exclusive_roles(self):
        for record in self:
            if record.library_assistant_id and record.worker_id:
                raise ValidationError('You can only select either Library Assistant or Worker, not both!')