from odoo import api, fields, models
from datetime import date


class Program135Merma(models.Model):
    _name = 'bm.ctl.produccion.merma'
    _description = 'Catalogo de Tipos de Mermas de Produccion (Program 135)'
    _order = 'categoria_global, codigo'

    name = fields.Char(
        string='Nombre',
        compute='_compute_name',
        store=True,
    )
    codigo = fields.Char(
        string='Codigo',
        required=True,
    )
    descripcion = fields.Char(
        string='Descripcion',
        required=True,
    )
    categoria_global = fields.Selection([
        ('LIQ', 'Merma Liquida (jarabe, agua, producto terminado)'),
        ('ENV', 'Merma de Envase (botellas, tapas, preformas)'),
        ('INS', 'Merma de Insumos (concentrados, aditivos, azucar)'),
        ('ETQ', 'Merma de Etiquetado (etiquetas, film termoencogible)'),
        ('EMP', 'Merma de Empaque (cajas, tarimas, exhibidores, poly stretch)'),
        ('CAL', 'Merma por Calidad (rechazo, pruebas)'),
        ('FOR', 'Merma por Cambio de Formato'),
        ('OTR', 'Otros'),
    ], string='Categoria Global', required=True, default='OTR')
    tipart_original = fields.Char(
        string='Tipart Original (Legacy)',
        help='Codigo tipart original del sistema legacy (001-051)',
    )
    activo = fields.Boolean(
        string='Activo',
        default=True,
    )
    porcentaje_estandar = fields.Float(
        string='Porcentaje Estandar (%)',
        help='Porcentaje de merma esperado/permitido',
    )
    recuperable = fields.Boolean(
        string='Recuperable',
        default=False,
        help='Si la merma es recuperable/reutilizable',
    )
    afecta_costo = fields.Boolean(
        string='Afecta Costo',
        default=True,
        help='Si la merma impacta el calculo de costos',
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

    @api.depends('codigo', 'descripcion')
    def _compute_name(self):
        for rec in self:
            rec.name = f'{rec.codigo} - {rec.descripcion}' if rec.codigo else rec.descripcion

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
