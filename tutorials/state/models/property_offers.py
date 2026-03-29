from dateutil.relativedelta import relativedelta
from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string='Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', default='accepted', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)


    validity = fields.Integer(string='Validity (days)', default=7, required=True)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True, required=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            base_date = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.context_today(offer)
            offer.date_deadline = base_date + relativedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            if not offer.date_deadline:
                continue
            base_date = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.context_today(offer)
            offer.validity = (offer.date_deadline - base_date).days