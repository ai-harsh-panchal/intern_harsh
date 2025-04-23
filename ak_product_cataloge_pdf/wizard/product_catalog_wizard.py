# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductCatalogWizard(models.TransientModel):
    """
    this model is used for products catalog details
    manage style and page break after for product catalog report
    """
    _name = 'product.catalog.wizard'
    _description = 'Product Catalog Wizard'
    catalog_style = fields.Selection([
        ('style_1', 'Style 1'),
        ('style_2', 'Style 2')
    ], string='Catalog Style', default='style_1')
    page_break_after = fields.Integer(string='Page Break After', default=5)
    product_ids = fields.Many2many('product.product', string='Products')

    @api.constrains('page_break_after')
    def check_page_break(self):
        """
        this function is manage the page break after
        if page break value is 0 then it will raise validation error
        """
        for record in self:
            if record.page_break_after <= 0:
                raise ValidationError('Page break should be greater than 0.')
