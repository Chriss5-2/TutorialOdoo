from odoo import api, fields, models


class Program162Solicitud(models.Model):
    _name = 'bm.ctl.produccion.formula.solicitud'
    _description = 'Solicitud de Activacion de Formulas (Program 162)'
    _order = 'fecha desc, id desc'

    name = fields.Char(
        string='Numero Documento',
        required=True,
        readonly=True,
        default='Nuevo',
        copy=False,
    )
    compania = fields.Char(
        string='Compania',
        required=True,
        default='0030',
    )
    transaccio = fields.Char(
        string='Transaccion',
        required=True,
        default='AFOR',
    )
    fecha = fields.Integer(
        string='Fecha (Juliano)',
        required=True,
        default=lambda self: self._default_fecha(),
    )
    fecha_display = fields.Date(
        string='Fecha',
        compute='_compute_fecha_display',
        store=False,
    )
    solicitante = fields.Integer(
        string='Solicitante (ID Empleado)',
        required=True,
    )
    solicitante_id = fields.Many2one(
        'hr.employee',
        string='Solicitante',
        compute='_compute_solicitante_info',
        store=False,
    )
    qarticulos = fields.Integer(
        string='Cantidad Articulos',
        compute='_compute_qarticulos',
        store=True,
    )
    qacciones = fields.Integer(
        string='Cantidad Acciones',
        compute='_compute_qacciones',
        store=True,
    )
    nivelapr = fields.Integer(
        string='Nivel Aprobacion',
        default=1,
    )
    aprobador = fields.Integer(
        string='Aprobador Actual (ID Empleado)',
    )
    fecaprobac = fields.Integer(
        string='Fecha Aprobacion (Juliano)',
        readonly=True,
    )
    horaprobac = fields.Char(
        string='Hora Aprobacion',
        readonly=True,
    )
    stsaprobac = fields.Selection([
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
        ('C', 'En Curso'),
    ], string='Status Aprobacion', default='P', required=True)
    stsactualiza = fields.Char(
        string='Status Actualizacion',
        default='P',
    )
    flganulado = fields.Boolean(
        string='Anulado',
        default=False,
    )
    fecanula = fields.Integer(
        string='Fecha Anulacion (Juliano)',
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
    ultusumod = fields.Char(
        string='Usuario Ultima Mod.',
        default=lambda self: self.env.user.login,
    )

    line_ids = fields.One2many(
        'bm.ctl.produccion.formula.solicitud.line',
        'solicitud_id',
        string='Lineas de Solicitud',
        copy=True,
    )
    firma_ids = fields.One2many(
        'bm.ctl.produccion.formula.firma',
        'solicitud_id',
        string='Firmas de Aprobacion',
        readonly=True,
    )

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('pending', 'En Aprobacion'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft', required=True)

    @api.model
    def _default_fecha(self):
        from datetime import date
        today = date.today()
        base = date(today.year, 1, 1)
        return (today - base).days + 730000

    @api.depends('fecha')
    def _compute_fecha_display(self):
        from datetime import date, timedelta
        for rec in self:
            if rec.fecha:
                base = date(rec.fecha - 730000 + (date(rec.fecha // 1000, 1, 1) - date(rec.fecha // 1000, 1, 1)).days, 1, 1)
                rec.fecha_display = base + timedelta(days=rec.fecha - 730000 - 1)
            else:
                rec.fecha_display = False

    @api.depends('solicitante')
    def _compute_solicitante_info(self):
        for rec in self:
            if rec.solicitante:
                emp = self.env['hr.employee'].search([('id', '=', rec.solicitante)], limit=1)
                rec.solicitante_id = emp if emp else False
            else:
                rec.solicitante_id = False

    @api.depends('line_ids')
    def _compute_qarticulos(self):
        for rec in self:
            rec.qarticulos = len(rec.line_ids.mapped('articulo'))

    @api.depends('line_ids')
    def _compute_qacciones(self):
        for rec in self:
            rec.qacciones = len(rec.line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('bm.formula.solicitud') or 'Nuevo'
        return super().create(vals_list)

    def action_submit(self):
        self.write({
            'state': 'pending',
            'stsaprobac': 'P',
        })

    def action_approve(self):
        now = fields.Datetime.now()
        self.write({
            'state': 'approved',
            'stsaprobac': 'A',
            'fecaprobac': self._default_fecha(),
            'horaprobac': now.strftime('%H%M%S'),
        })
        for firma in self.firma_ids.filtered(lambda f: f.stsaprobac == 'P'):
            firma.write({
                'stsaprobac': 'A',
                'fecautoriz': self._default_fecha(),
                'horautoriz': now.strftime('%H%M%S'),
            })

    def action_reject(self):
        self.write({
            'state': 'rejected',
            'stsaprobac': 'R',
        })

    def action_cancel(self):
        self.write({
            'state': 'cancelled',
            'flganulado': True,
            'fecanula': self._default_fecha(),
        })

    def action_reset_to_draft(self):
        self.write({
            'state': 'draft',
            'stsaprobac': 'P',
        })
