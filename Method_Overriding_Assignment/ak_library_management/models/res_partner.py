# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    """
    inherit the res partner model for add boolean field
    """
    _inherit = 'res.partner'

    not_trust_worthy = fields.Boolean(string='Not Trustworthy')
    is_member = fields.Boolean(string='Is Member')
    is_librarian = fields.Boolean(string='Is Librarian')
