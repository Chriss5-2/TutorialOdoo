from odoo import api, fields, models


class Program162SolicitudLine(models.Model):
    _name = 'bm.ctl.produccion.formula.solicitud.line'
    _description = 'Linea de Solicitud de Formula (Program 162 - Detalle)'

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
    sucform = fields.Char(
        string='Sucursal Formula',
        required=True,
        default='0001',
    )
    articulo = fields.Float(
        string='Articulo (SKU)',
        required=True,
        digits='Product Unit of Measure',
    )
    insumo = fields.Float(
        string='Insumo (Material)',
        required=True,
        digits='Product Unit of Measure',
    )
    linea = fields.Char(
        string='Linea',
    )
    factconv = fields.Float(
        string='Factor Conversion',
        digits='Product Unit of Measure',
    )
    accion = fields.Selection([
        ('N', 'Nuevo'),
        ('M', 'Modificar'),
        ('E', 'Eliminar'),
    ], string='Accion', default='N', required=True)
    nivapro = fields.Integer(
        string='Nivel Aprobacion',
        default=1,
    )
    flgaprob = fields.Boolean(
        string='Aprobado',
        default=False,
    )
    aprobadop = fields.Integer(
        string='Aprobado Por (ID Empleado)',
    )
    fecaprob = fields.Integer(
        string='Fecha Aprobacion (Juliano)',
    )
    horaprob = fields.Char(
        string='Hora Aprobacion',
    )
    stssolicitud = fields.Selection([
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    ], string='Status Solicitud', default='P')
    progactfor = fields.Char(
        string='Programa Activacion Formula',
        default='162',
    )
    seleccion = fields.Binary(
        string='Seleccion',
    )
    elimreg = fields.Boolean(
        string='Eliminar Registro',
        default=False,
    )

    articulo_display = fields.Char(
        string='Articulo',
        compute='_compute_articulo_display',
    )
    insumo_display = fields.Char(
        string='Insumo',
        compute='_compute_insumo_display',
    )

    @api.depends('articulo')
    def _compute_articulo_display(self):
        for rec in self:
            rec.articulo_display = str(int(rec.articulo)) if rec.articulo else ''

    @api.depends('insumo')
    def _compute_insumo_display(self):
        for rec in self:
            rec.insumo_display = str(int(rec.insumo)) if rec.insumo else ''
