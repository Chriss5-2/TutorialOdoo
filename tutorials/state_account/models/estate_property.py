from odoo import models, Command

class InheritedModel(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for property_record in self:
            self.env["account.move"].create(
            {
                "partner_id": property_record.buyer_id.id,
                "move_type": "out_invo ice",
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Comision venta: {property_record.name}",
                        "quantity": 1,
                        "price_unit": property_record.selling_price * 0.06,
                    }),
                    Command.create({
                        "name": "Gastos administrativos",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ]
            })
        return super().action_set_sold()