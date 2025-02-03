from odoo import models, fields


class Book(models.Model):
    _name = 'library.book'
    _description = 'Book Model'

    name = fields.Char(string='Book Title', required=True)
    author = fields.Char(string='Author Name')
    isbn = fields.Char(string='ISBN Number')
    publication_date = fields.Date(string='Date of Publication')
    category_id = fields.Many2one('library.category', string='Book Category')
    description = fields.Text(string='Book Summary')
    state = fields.Selection([('available', 'Available'), ('borrowed', 'Borrowed'), ('lost', 'Lost')], string='State', default='available')
    tag_ids = fields.Many2many('library.tag', string='Tags', related='category_id.tag_ids', readonly=False)

class Tag(models.Model):
    _name = 'library.tag'
    _description = 'Library Tag'

    name = fields.Char(string='Tag Name', required=True)
    description = fields.Text(string='Tag Description')


class Category(models.Model):
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Category Description')
    tag_ids = fields.Many2many('library.tag', string='Tags')

