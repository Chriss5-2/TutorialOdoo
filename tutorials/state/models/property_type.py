from odoo import models, fields, api

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
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    sequence = fields.Integer(string='Sequence', default=1)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)