from odoo import api, fields, models
from datetime import date, timedelta


class Program132TurnoHorario(models.Model):
    _name = 'bm.ctl.produccion.turno.horario'
    _description = 'Horarios de Turno por Sucursal (Program 132)'
    _order = 'sucursal, turno_id, id'

    name = fields.Char(
        string='Nombre',
        required=True,
        compute='_compute_name',
        store=True,
    )
    sucursal = fields.Char(
        string='Sucursal',
        required=True,
    )
    turno_id = fields.Many2one(
        'bm.ctl.produccion.turno.definicion',
        string='Turno',
        required=True,
        ondelete='cascade',
    )
    codturno = fields.Integer(
        string='Codigo Turno',
        related='turno_id.codturno',
        store=True,
    )
    horainicio = fields.Char(
        string='Hora Inicio',
        related='turno_id.horainicio',
        store=False,
    )
    horafin = fields.Char(
        string='Hora Fin',
        related='turno_id.horafin',
        store=False,
    )
    esnocturno = fields.Boolean(
        string='Es Nocturno',
        related='turno_id.esnocturno',
        store=False,
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

    @api.depends('sucursal', 'turno_id')
    def _compute_name(self):
        for rec in self:
            if rec.turno_id:
                rec.name = f'{rec.sucursal} - {rec.turno_id.name}'
            else:
                rec.name = f'{rec.sucursal} - Sin Turno'

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
