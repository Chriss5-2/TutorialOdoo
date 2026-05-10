from odoo import api, fields, models


class Program162Firma(models.Model):
    _name = 'bm.ctl.produccion.formula.firma'
    _description = 'Firmas de Aprobacion de Formulas (Program 162 - Trazabilidad)'
    _order = 'nivel, feccrea'

    solicitud_id = fields.Many2one(
        'bm.ctl.produccion.formula.solicitud',
        string='Solicitud',
        required=True,
        ondelete='cascade',
    )
    compania = fields.Char(
        string='Compania',
        related='solicitud_id.compania',
        store=True,
    )
    transaccio = fields.Char(
        string='Transaccion',
        related='solicitud_id.transaccio',
        store=True,
    )
    nrodoc = fields.Char(
        string='Numero Documento',
        related='solicitud_id.name',
        store=True,
    )
    articulo = fields.Float(
        string='Articulo (SKU)',
        digits='Product Unit of Measure',
    )
    insumo = fields.Float(
        string='Insumo (Material)',
        digits='Product Unit of Measure',
    )
    sucform = fields.Char(
        string='Sucursal Formula',
    )
    lineainsumo = fields.Char(
        string='Linea Insumo',
    )
    nivel = fields.Integer(
        string='Nivel Aprobacion',
        required=True,
    )
    empleautor = fields.Integer(
        string='Empleado Autorizador (ID)',
    )
    empleautor_id = fields.Many2one(
        'hr.employee',
        string='Empleado Autorizador',
        compute='_compute_empleautor_info',
    )
    fecautoriz = fields.Integer(
        string='Fecha Autorizacion (Juliano)',
    )
    horautoriz = fields.Char(
        string='Hora Autorizacion',
    )
    stsaprobac = fields.Selection([
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
        ('C', 'En Curso'),
    ], string='Status Aprobacion', default='P', required=True)
    observac = fields.Text(
        string='Observaciones',
    )
    estado = fields.Selection([
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ], string='Estado', default='A', required=True)
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
    horultimod = fields.Char(
        string='Hora Ultima Mod.',
        default=lambda self: fields.Datetime.now().strftime('%H%M%S'),
    )
    ultusumod = fields.Char(
        string='Usuario Ultima Mod.',
        default=lambda self: self.env.user.login,
    )

    @api.model
    def _default_fecha(self):
        from datetime import date
        today = date.today()
        base = date(today.year, 1, 1)
        return (today - base).days + 730000

    @api.depends('empleautor')
    def _compute_empleautor_info(self):
        for rec in self:
            if rec.empleautor:
                emp = self.env['hr.employee'].search([('id', '=', rec.empleautor)], limit=1)
                rec.empleautor_id = emp if emp else False
            else:
                rec.empleautor_id = False
