from odoo import api, fields, models


class Program162TmpDetalle(models.Model):
    _name = 'bm.ctl.produccion.formula.tmp.detalle'
    _description = 'Detalle Temporal de Formulas (Program 162 - Proceso)'

    clave = fields.Char(
        string='Clave',
        required=True,
    )
    compania = fields.Char(
        string='Compania',
    )
    transaccio = fields.Char(
        string='Transaccion',
    )
    nrodoc = fields.Char(
        string='Numero Documento',
    )
    sucform = fields.Char(
        string='Sucursal Formula',
    )
    articulo = fields.Float(
        string='Articulo (SKU)',
        digits='Product Unit of Measure',
    )
    insumo = fields.Float(
        string='Insumo (Material)',
        digits='Product Unit of Measure',
    )
    linea = fields.Char(
        string='Linea',
    )
    factconv = fields.Float(
        string='Factor Conversion',
        digits='Product Unit of Measure',
    )
    accion = fields.Char(
        string='Accion',
    )
    nivapro = fields.Integer(
        string='Nivel Aprobacion',
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
    stssolicitud = fields.Char(
        string='Status Solicitud',
    )
    progactfor = fields.Char(
        string='Programa Activacion Formula',
    )
    seleccion = fields.Binary(
        string='Seleccion',
    )
    elimreg = fields.Boolean(
        string='Eliminar Registro',
        default=False,
    )

    _sql_constraints = [
        ('unique_tmpdetfor',
         'unique(clave, compania, transaccio, nrodoc, sucform, articulo, insumo)',
         'Ya existe un registro temporal para esta combinacion'),
    ]
