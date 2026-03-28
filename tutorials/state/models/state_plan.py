from odoo import fields, models

class StatePlan(models.Model):
    _name='estate.property'
    _description='State Plan'

    name = fields.Char(string='Name', required=True)
    num_months = fields.Integer(string='Number of Months', required=True)
    active = fields.Boolean(string='Active', default=True)
    expected_price = fields.Float(string='Expected Price', required=True)