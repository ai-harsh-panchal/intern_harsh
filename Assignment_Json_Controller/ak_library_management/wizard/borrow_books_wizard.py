# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BorrowBooksWizard(models.Model):
    _name = 'borrow.books.wizard'
    _description = 'Wizard for Borrowing Books'

    message = fields.Text(string="Wizard Message", readonly=True)
    borrow_wizard_id = fields.Many2one(comodel_name='borrow.transaction.history', string="Borrow Transaction")
    next_action = fields.Text(string="Next Action", readonly=True)

    def action_continue(self):
        """ Handles the 'Continue' button:
        - If more warnings exist, display them sequentially.
        - If no more warnings, finalize the borrow transaction.
        param: self
        Returns: dict: Action to display the next warning or finalize the transaction.
        """
        next_warnings = eval(self.next_action) if self.next_action else []
        if next_warnings:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Warning',
                'res_model': 'borrow.books.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_borrow_wizard_id': self.borrow_wizard_id.id,
                    'default_message': next_warnings[0],
                    'default_next_action': repr(next_warnings[1:]) if len(next_warnings) > 1 else None
                }
            }
        else:
            # No more warnings, proceed with the transaction
            return self.borrow_wizard_id._process_borrow_transaction()

    def action_cancel(self):
        """Handles the cancel action, which closes the wizard."""
        return {'type': 'ir.actions.act_window_close'}
