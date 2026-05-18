from odoo import api, fields, models
from datetime import date


class Program135MermaRegistro(models.Model):
    _name = 'bm.ctl.produccion.merma.registro'
    _description = 'Registro Transaccional de Mermas de Produccion (Program 135)'
    _order = 'fecha desc, id desc'

    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True,
    )
    nroop = fields.Char(
        string='Orden de Produccion',
        required=True,
        help='Numero de orden de produccion asociada',
    )
    tipo_merma_id = fields.Many2one(
        'bm.ctl.produccion.merma',
        string='Tipo de Merma',
        required=True,
    )
    insumo_codigo = fields.Integer(
        string='Codigo Insumo',
        required=True,
        help='Codigo del insumo (maestro de articulos)',
    )
    insumo_descripcion = fields.Char(
        string='Descripcion Insumo',
    )
    linea = fields.Char(
        string='Linea de Produccion',
    )
    turno = fields.Char(
        string='Turno',
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.context_today,
    )
    cantidad_std = fields.Float(
        string='Cantidad Estandar',
        digits='Product Unit of Measure',
        required=True,
        default=0.0,
    )
    cantidad_real = fields.Float(
        string='Cantidad Real',
        digits='Product Unit of Measure',
        required=True,
        default=0.0,
    )
    cantidad_merma = fields.Float(
        string='Cantidad Merma',
        compute='_compute_cantidad_merma',
        store=True,
        digits='Product Unit of Measure',
    )
    porcentaje_merma = fields.Float(
        string='Porcentaje Merma (%)',
        compute='_compute_porcentaje_merma',
        store=True,
    )
    costo_estandar = fields.Float(
        string='Costo Estandar Unitario',
        digits='Product Price',
        default=0.0,
    )
    costo_merma = fields.Float(
        string='Costo Merma',
        compute='_compute_costo_merma',
        store=True,
        digits='Product Price',
    )
    observaciones = fields.Text(
        string='Observaciones',
        help='Causa y detalles de la merma',
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

    @api.depends('nroop', 'tipo_merma_id')
    def _compute_name(self):
        for rec in self:
            tipo = rec.tipo_merma_id.codigo if rec.tipo_merma_id else 'S/T'
            rec.name = f'{rec.nroop} - {tipo}' if rec.nroop else tipo

    @api.depends('cantidad_std', 'cantidad_real')
    def _compute_cantidad_merma(self):
        for rec in self:
            rec.cantidad_merma = rec.cantidad_real - rec.cantidad_std

    @api.depends('cantidad_std', 'cantidad_merma')
    def _compute_porcentaje_merma(self):
        for rec in self:
            if rec.cantidad_std != 0:
                rec.porcentaje_merma = (rec.cantidad_merma / rec.cantidad_std) * 100
            else:
                rec.porcentaje_merma = 0.0

    @api.depends('cantidad_merma', 'costo_estandar')
    def _compute_costo_merma(self):
        for rec in self:
            rec.costo_merma = rec.cantidad_merma * rec.costo_estandar

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

    def action_save_and_close(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}
