from odoo import models, fields

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type"
    _order = 'sequence, name, id'

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.'
    )


    name = fields.Char(string='Name', required=True)


    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    sequence = fields.Integer(string='Sequence', default=1)