from dateutil.relativedelta import relativedelta
from odoo import fields, models
from odoo import api
from odoo.exceptions import UserError

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

    tag_ids = fields.Many2many('estate.property.tag', string='Tags', store=True, copy=False)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', copy=False, store=True)


    living_area = fields.Float(string='Living Area (sqm)', required=True)
    garden_area = fields.Float(string='Garden Area (sqm)', required=True)
    total_area = fields.Float(compute='_compute_total_area', string='Total Area (sqm)', store=True, readonly=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    best_price = fields.Float(string='Best Offer', compute='_compute_best_price', store=True, readonly=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Orientation', required=True)
    garden = fields.Boolean(string='Has Garden?', required=True, default=False)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self.orientation = 'north'
        else:
            self.garden_area = 0.0
            self.orientation = False

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('A cancelled property cannot be set as sold.')
            record.state = 'sold'
        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be cancelled.')
            record.state = 'cancelled'
        return True