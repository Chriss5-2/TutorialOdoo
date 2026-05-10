from odoo import api, fields, models


class Program162AprobadorConfig(models.Model):
    _name = 'bm.ctl.produccion.formula.aprobador.config'
    _description = 'Configuracion de Aprobadores de Formulas (Program 162)'

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
    nivel = fields.Integer(
        string='Nivel',
        required=True,
    )
    tipaprob = fields.Selection([
        ('L', 'Lineal'),
        ('P', 'Paralelo'),
    ], string='Tipo Aprobacion', default='L', required=True)
    aprobador = fields.Integer(
        string='Aprobador (ID Empleado)',
        required=True,
    )
    aprobador_id = fields.Many2one(
        'hr.employee',
        string='Aprobador',
        compute='_compute_aprobador_info',
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

    _sql_constraints = [
        ('unique_aprobador_nivel',
         'unique(compania, transaccio, nivel, tipaprob, aprobador)',
         'Ya existe un aprobador configurado para este nivel y tipo'),
    ]

    @api.model
    def _default_fecha(self):
        from datetime import date
        today = date.today()
        base = date(today.year, 1, 1)
        return (today - base).days + 730000

    @api.depends('aprobador')
    def _compute_aprobador_info(self):
        for rec in self:
            if rec.aprobador:
                emp = self.env['hr.employee'].search([('id', '=', rec.aprobador)], limit=1)
                rec.aprobador_id = emp if emp else False
            else:
                rec.aprobador_id = False
