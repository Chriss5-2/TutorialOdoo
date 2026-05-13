from odoo import api, fields, models
from datetime import date, timedelta


class Program132TurnoDefinicion(models.Model):
    _name = 'bm.ctl.produccion.turno.definicion'
    _description = 'Catalogo de Turnos de Produccion (Program 132)'
    _order = 'secuencia, id'

    name = fields.Char(
        string='Nombre',
        compute='_compute_name',
        store=True,
    )
    codturno = fields.Integer(
        string='Codigo Turno',
        required=True,
    )
    descripcion = fields.Char(
        string='Descripcion',
        required=True,
        default='Turno sin descripcion',
    )
    secuencia = fields.Integer(
        string='Secuencia',
        required=True,
        default=10,
    )
    horainicio = fields.Char(
        string='Hora Inicio',
        default='060000',
    )
    horafin = fields.Char(
        string='Hora Fin',
        default='140000',
    )
    esnocturno = fields.Boolean(
        string='Es Nocturno (Cruza dia)',
        compute='_compute_esnocturno',
        store=True,
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

    @api.depends('codturno', 'descripcion')
    def _compute_name(self):
        for rec in self:
            rec.name = f'T{rec.codturno:03d} - {rec.descripcion}' if rec.codturno else rec.descripcion

    @api.depends('horainicio', 'horafin')
    def _compute_esnocturno(self):
        for rec in self:
            if rec.horainicio and rec.horafin:
                rec.esnocturno = rec.horainicio > rec.horafin
            else:
                rec.esnocturno = False

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
