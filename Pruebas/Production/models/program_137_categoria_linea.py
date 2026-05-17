from odoo import api, fields, models
from datetime import date


class Program137CategoriaLinea(models.Model):
    _name = 'bm.ctl.produccion.categoria.linea'
    _description = 'Categoria de Linea de Produccion (Program 137)'
    _order = 'efamilia'

    name = fields.Char(
        string='Nombre',
        compute='_compute_name',
        store=True,
    )
    efamilia = fields.Char(
        string='Codigo',
        required=True,
    )
    descripcion = fields.Char(
        string='Descripcion',
        required=True,
        default='Sin descripcion',
    )
    area = fields.Char(
        string='Area Funcional',
    )
    factor = fields.Selection([
        ('B', 'Botella'),
        ('N', 'No Botella'),
    ], string='Factor')
    funcion = fields.Selection([
        ('N', 'Normal'),
        ('G', 'Global'),
    ], string='Funcion', default='N')
    almproc = fields.Char(
        string='Almacen de Proceso',
    )
    activo = fields.Boolean(
        string='Activo',
        default=True,
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

    @api.depends('efamilia', 'descripcion')
    def _compute_name(self):
        for rec in self:
            rec.name = f'{rec.efamilia} - {rec.descripcion}' if rec.efamilia else rec.descripcion

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
