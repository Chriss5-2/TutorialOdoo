from odoo import models, fields

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type"

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.'
    )


    name = fields.Char(string='Name', required=True)