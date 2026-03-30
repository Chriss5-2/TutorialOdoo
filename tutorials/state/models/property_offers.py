from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string='Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', copy=False)
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

    def action_accept(self):
        for offer in self:
            accepted_offer = self.search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted'),
                ('id', '!=', offer.id),
            ], limit=1)

            if accepted_offer:
                raise UserError('Only one offer can be accepted for a property.')

            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True