from odoo import api, fields, models
from datetime import date


class Sucursal(models.Model):
    _name = 'bm.sucursal'
    _description = 'Sucursal'
    _order = 'codigo'

    name = fields.Char(
        string='Nombre',
        compute='_compute_name',
        store=True,
    )
    codigo = fields.Char(
        string='Codigo',
        required=True,
    )
    nombre = fields.Char(
        string='Nombre Descriptivo',
    )
    activo = fields.Boolean(
        string='Activo',
        default=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Compania',
        default=lambda self: self.env.company,
    )
    feccrea = fields.Integer(
        string='Fecha Creacion (Juliano)',
        required=True,
        default=lambda self: self._default_fecha(),
    )
    horcrea = fields.Char(
        string='Hora Creacion',
        required=True,
        default=lambda self: fields.Datetime.now().strftime('%H%M%S'),
    )
    usucrea = fields.Char(
        string='Usuario Creacion',
        required=True,
        default=lambda self: self.env.user.login,
    )
    fecultmod = fields.Integer(
        string='Fecha Ultima Mod. (Juliano)',
        default=lambda self: self._default_fecha(),
    )
    horultmod = fields.Char(
        string='Hora Ultima Mod.',
        default=lambda self: fields.Datetime.now().strftime('%H%M%S'),
    )
    usuaulmod = fields.Char(
        string='Usuario Ultima Mod.',
        default=lambda self: self.env.user.login,
    )

    @api.model
    def _default_fecha(self):
        today = date.today()
        base = date(today.year, 1, 1)
        return (today - base).days + 730000

    @api.depends('codigo', 'nombre')
    def _compute_name(self):
        for rec in self:
            if rec.codigo and rec.nombre:
                rec.name = f'{rec.codigo} - {rec.nombre}'
            else:
                rec.name = rec.codigo or rec.nombre or ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('usucrea'):
                vals['usucrea'] = self.env.user.login
            if not vals.get('feccrea'):
                vals['feccrea'] = self._default_fecha()
            if not vals.get('horcrea'):
                vals['horcrea'] = fields.Datetime.now().strftime('%H%M%S')
        return super().create(vals_list)

    def write(self, vals):
        if not vals.get('usuaulmod'):
            vals['usuaulmod'] = self.env.user.login
        if not vals.get('fecultmod'):
            vals['fecultmod'] = self._default_fecha()
        if not vals.get('horultmod'):
            vals['horultmod'] = fields.Datetime.now().strftime('%H%M%S')
        return super().write(vals)
