from odoo import api, fields, models
from datetime import date, timedelta


class Program132ProduccionConfig(models.Model):
    _name = 'bm.ctl.produccion.config'
    _description = 'Configuracion Global de Produccion (Program 132)'
    _order = 'compania, id'

    name = fields.Char(
        string='Nombre',
        required=True,
        compute='_compute_name',
        store=True,
    )
    compania = fields.Char(
        string='Compania',
        required=True,
        default='0030',
    )
    fecha_inicial_prod = fields.Integer(
        string='Fecha Inicial Produccion (Juliano)',
        help='Fecha desde la cual se migran/muestran datos de produccion',
        default=lambda self: self._default_fecha(),
    )
    fecha_inicial_prod_display = fields.Date(
        string='Fecha Inicial',
        compute='_compute_fecha_display',
        store=False,
    )
    turno_default_id = fields.Many2one(
        'bm.ctl.produccion.turno.definicion',
        string='Turno por Defecto',
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

    @api.depends('compania')
    def _compute_name(self):
        for rec in self:
            rec.name = f'Config Produccion - {rec.compania}'

    @api.depends('fecha_inicial_prod')
    def _compute_fecha_display(self):
        for rec in self:
            if rec.fecha_inicial_prod:
                days_since_jan1 = rec.fecha_inicial_prod - 730000
                year = rec.fecha_inicial_prod // 1000
                try:
                    base = date(year, 1, 1)
                    rec.fecha_inicial_prod_display = base + timedelta(days=days_since_jan1 - 1)
                except (ValueError, OverflowError):
                    rec.fecha_inicial_prod_display = False
            else:
                rec.fecha_inicial_prod_display = False

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
