from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = 'name asc'

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property tag name must be unique.'
    )

    name = fields.Char(string='Name', required=True)