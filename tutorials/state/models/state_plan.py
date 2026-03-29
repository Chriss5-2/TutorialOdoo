from dateutil.relativedelta import relativedelta
from odoo import fields, models

class StatePlan(models.Model):
    _name='estate.property'
    _description='State Plan'

    name = fields.Char(string='Name', required=True)
    num_months = fields.Integer(string='Number of Months', required=True, default=3)
    active = fields.Boolean(string='Active', default=True)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, default=0.0, copy=False)
    availability_date = fields.Date(string='Availability Date', default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    num_bedrooms = fields.Integer(string='Number of Bedrooms', required=True, default=2)

    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        required=True,
        copy=False,
        default='new'
    )

    description = fields.Text(string='Description', required=True)
    
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')


    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user, copy=False)

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')