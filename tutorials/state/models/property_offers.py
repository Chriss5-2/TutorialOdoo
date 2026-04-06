from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = 'price desc'

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive.'
    )

    price = fields.Float(string='Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        related='property_id.property_type_id',
        store=True,
        readonly=True,
    )


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

    @api.model_create_multi
    def create(self, vals_list):
        property_model = self.env['estate.property']
        # Verifica cada oferta para asegurarse de que no se cree una oferta con un precio menor que la mejor oferta existente para la propiedad
        for vals in vals_list:
            property_id = vals.get('property_id')
            price = vals.get('price', 0.0)

            if not property_id:
                continue

            # vals['property_id'] is an int; browse turns it into a recordset.
            property_record = property_model.browse(property_id)
            if property_record.offer_ids:
                best_existing_offer = max(property_record.offer_ids.mapped('price'))
                # Verifica si el nuevo precio es menor que la mejor oferta existente
                # En caso sea menor, se lanza una excepción para impedir la creación de la oferta
                # Si es mayor o igual, se permite la creación de la oferta
                if price < best_existing_offer:
                    raise ValidationError('You cannot create an offer lower than an existing one.')

        # Si todas las ofertas son válidas, se procede a crear las ofertas utilizando el método create del modelo padre
        offers = super().create(vals_list)
        # Si el estado de la propiedad es 'new', se cambia a 'offer_received' al crear una nueva oferta
        offers.mapped('property_id').filtered(lambda p: p.state == 'new').write({'state': 'offer_received'})
        return offers

    def action_accept(self):
        for offer in self:
            if offer.property_id.state in ('cancelled', 'sold'):
                raise UserError('You cannot accept an offer for a cancelled or sold property.')

            accepted_offer = self.search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted'),
                ('id', '!=', offer.id),
            ], limit=1)

            if accepted_offer:
                raise UserError('Only one offer can be accepted for a property.')

            # Si la oferta es válida para ser aceptada, se actualiza el estado de la oferta a 'accepted', se asigna el comprador a la propiedad, se establece el precio de venta y se cambia el estado de la propiedad a 'offer_accepted'
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            if offer.property_id.state in ('cancelled', 'sold'):
                raise UserError('You cannot refuse an offer for a cancelled or sold property.')
            offer.status = 'refused'
        return True