# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def button_confirm(self):
        low_stock_books = []
        for line in self.order_line:
            if line.product_id.type == 'product' and line.product_id.qty_available < 5:
                low_stock_books.append(line.product_id.name)

        if low_stock_books:
            warning_message = "The following books are low in stock: " + ", ".join(low_stock_books)
            return {
                'warning': {
                    'title': "Low Stock Warning",
                    'message': warning_message,
                }
            }

        return super(SaleOrder, self).button_confirm()

    def action_approve(self):
        self.state = 'sale'

    def action_reject(self):
        self.state = 'cancel'
