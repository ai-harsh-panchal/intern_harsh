# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Member(models.Model):
    """
    this model is used for add the member for library
    """
    _name = 'library.member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Member Model'

    member_id = fields.Many2one(comodel_name='res.partner', string='Member Name', required=True)
    email = fields.Char(string='Email ID', related='member_id.email')
    phone = fields.Char(string='Contact Number')
    membership_date = fields.Date(string='Membership Start Date')
    book_ids = fields.Many2many(comodel_name='library.book', string='Books')
    membership_no = fields.Char(string='membership_no', readonly=True)

    @api.model_create_multi
    def create(self,vals_list):
        """
        this method is used to generate unique sequence for member record
        parameter: self
        return: base create orm method
        return type: recordset
        """
        for vals in vals_list:
            vals['membership_no'] = self.env['ir.sequence'].next_by_code('library.member')
        return super(Member, self).create(vals_list)

    def action_send_mail(self):
        """
        this method is used to send mail to member when membership is expired
        parameter: self
        return: dictionary of action and open form
        """
        self.ensure_one()
        librarian_user = self.env.user
        if not librarian_user.is_librarian:
            raise ValidationError('you are not librarian to send mail')
        template_id = self.env.ref('ak_library_management.email_template_library_member_renewal').id
        composer = {
            'default_template_id': template_id,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': composer,
        }

