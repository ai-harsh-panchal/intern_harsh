# -*- coding: utf-8 -*-

from odoo import models, fields,api


class ResPartner(models.Model):
    """
    inherit the res partner model for add boolean field
    """
    _inherit = 'res.partner'

    not_trust_worthy = fields.Boolean(string='Not Trustworthy')
    is_member = fields.Boolean(string='Is Member')
    is_librarian = fields.Boolean(string='Is Librarian')
    name_slugified = fields.Char(string='Slug', compute='_compute_name_slugified', store=True)

    @api.depends("name")
    def _compute_name_slugified(self):
        """
        this function is used for slugify the partner name in url path
        param : self
        return : none
        """
        for rec in self:
            rec.name_slugified = self.env['ir.http']._slugify(rec.name or '')