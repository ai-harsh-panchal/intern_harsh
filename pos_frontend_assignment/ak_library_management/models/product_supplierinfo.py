# -*- coding: utf-8 -*-

from odoo import models, fields,api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.model
    def create(self, vals):
        """
        Override create to enforce vendor assignment logic
        """
        product_tmpl_id = vals.get('product_tmpl_id')
        product_id = vals.get('product_id')

        if product_tmpl_id and product_id:
            product_tmpl = self.env['product.template'].browse(product_tmpl_id)
            product = self.env['product.product'].browse(product_id)
            if product_tmpl.is_vendor and product.product_tmpl_id.id == product_tmpl_id:
                vals['product_id'] = False
            elif not product_tmpl.is_vendor and product.product_tmpl_id.id == product_tmpl_id:
                vals['product_tmpl_id'] = False

        return super(ProductSupplierinfo, self).create(vals)