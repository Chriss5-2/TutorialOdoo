## Analisis Post-Implementacion - Program #138 (Familia de Produccion)

### Contexto de Validacion
Se ejecutáron ~45 consultas SQL exhaustivas contra la base de datos legacy `mxbdaje_local` para rastrear la arquitectura de configuracion de familias de produccion por sucursal. Revisar [validacion_program_138.md](data_para_agente/validaciones_programs/validacion_program_138.md) para el detalle completo de cada query (secciones 1-11) y la resolucion de las 5 dudas post-analisis.

La investigacion revelo que la "Familia de Produccion" del Program #138 **no es** un catalogo de familias de articulo (gaseosas, jugos, agua) como sugeria la documentacion de funciones, sino una **configuracion que activa/desactiva categorias de lineas de produccion por sucursal**, usando la tabla `sucproc` del legacy.

### Logica de Validacion y Hallazgos Tecnicos

La validacion se realizo mediante un proceso de **descarte sistematico y descubrimiento** en nueve etapas, partiendo desde cero por la ausencia de documentacion oficial:

1. **Exploracion de documentacion oficial**: Se busco en `aje_docs_simulacion/01_Docs_Oficiales/` referencias al Program #138 o concepto "familia de produccion".
    - Resultado: **0 coincidencias funcionales**. Solo referencias a stored procedures legacy (12 objetos con "familia" en el nombre), la mayoria codigo muerto.
    - Ubicacion en arbol de menus: `Mantenimiento → Configuraciones → Familia de Produccion`.
    - Conclusion: La fuente de verdad es exclusivamente la BD legacy.

2. **Busqueda de tablas con "familia"**: Se ejecutaron consultas con patrones `%familia%`, `bfamilia%`, `tipfamil%`.
    - Solo `ctm_familiaeq` contiene "familia" en el nombre de tabla (5.1).
    - No existe tabla maestra tipo `bfamilia1f` o `tipfamilia` (2.2).
    - 215 columnas en 100+ tablas contienen "familia" en su nombre (2.3).
    - Conclusion: El concepto "familia" esta disperso en multiples contextos (inventario, costos, equipos).

3. **Descarte de `mfamil1f` (familias de inventario)**: Se inspecciono estructura DDL y contenido.
    - PK: `(compania, linea, familia)` — jerarquia de inventario contable.
    - 25 lineas de inventario: Producto Terminado (01), Materia Prima (04), Envases (05), etc.
    - Familias: AZUCAR, JARABES, GASEOSA, PREFORMAS — clasificacion contable, no de produccion.
    - Conclusion: **NO es la tabla del Program #138**. Es el catalogo de familias de articulo. Descartada.

4. **Descarte de `msubfa1f` (subfamilias de inventario)**: Subcatalogo de `mfamil1f`.
    - PK: `(compania, linea, familia, subfamilia)`, 911 registros para Mexico.
    - Clasificacion contable con campos de compra local/importacion.
    - Conclusion: **NO es la tabla del Program #138**. Descartada.

5. **Descarte de `ctm_familiaeq` (familia equipo por ejercicio)**: Solo tabla con "familia" en el nombre.
    - PK: `(compania, sucursal, ejercicio, efamilia)`.
    - 0 registros para Mexico (0030). Tiene datos para otras compañias (0002=252 registros) pero nunca se uso en MX.
    - Conclusion: **NO es la tabla del Program #138**. Configuracion de costeo vacia para MX. Descartada.

6. **Analisis de `martic1f` (maestro de articulos)**: Verificacion de campos de produccion.
    - `tipartprod` (tipo articulo produccion): 9 valores distintos, domina valor 9 con 25,981 articulos.
    - `linfabric` (linea fabricacion): 15 valores, domina valor 1 con 15,225 articulos.
    - NO existe columna `famprod` en `martic1f` — la familia de produccion no es propiedad del articulo.
    - Conclusion: El concepto de "familia de produccion" esta en el contexto de costeo, no del maestro de articulos.

7. **Hallazgo principal: `cabstdpro.famprod` = `mfameq1f.efamilia`**:
    - `cabstdpro.famprod` (costeo estandar) tiene 12 valores para MX.
    - Correspondencia **1:1 perfecta** con `mfameq1f.efamilia` (familia de equipo, Program #137).
    - Las 12 familias de `cabstdpro` son exactamente las mismas que `mfameq1f`.
    - Conclusion: La "familia de produccion" en la BD legacy ES la familia de equipo del Program #137.

8. **Rastreo de `efamilia` en todas las tablas**: Se identificaron 9 tablas con columna `efamilia`.
    - `mfameq1f`: catalogo de familias de equipo (Program #137, 27 categorias).
    - `drplinpro`: DRP planificacion — vacia para MX.
    - `tactpr1f`: transacciones actividad — vacia para MX.
    - `tparman`: parametros mantenimiento/OEE — vacia para MX.
    - `sucproc`: **16 registros para Mexico — LA TABLA DEL PROGRAM #138**.
    - Conclusion: Solo `sucproc` tiene datos operativos para Mexico 0030.

9. **Confirmacion de `sucproc` como tabla del Program #138**:
    - PK: `(compania, sucursal, efamilia)` — unicidad por sucursal + familia.
    - 16 registros: 4 sucursales × 4 familias.
    - Sucursales activas: 0001, 0068, 0070, 0108.
    - Familias configuradas: 001 (ENVASADO), 003 (JARABES), 019 (MAQUILA), 021 (REEMPAQUES).
    - Solo 2 campos de negocio adicionales a la PK: `estado` (A/I) y auditoria.
    - Conclusion: `sucproc` es una tabla de activacion/desactivacion — configura que familias de produccion operan en cada sucursal.

### Tabla Resumen de Hallazgos Legacy

| Tabla | Registros | Proposito Esperado | Estado Real |
|---|---|---|---|
| `mfamil1f` | ~800 | Catalogo de familias de produccion | **Descartada** — familias de inventario contable |
| `msubfa1f` | 911 | Subcatalogo de familias | **Descartada** — subfamilias de inventario |
| `ctm_familiaeq` | 0 (MX) | Configuracion familia-equipo por ejercicio | **Descartada** — vacia para Mexico 0030 |
| `mfameq1f` | 397 (MX) | Catalogo de familias de equipo | **Tabla del Program #137** — ya migrada como `bm.ctl.produccion.categoria.linea` |
| `cabstdpro` | con `famprod` | Costeo estandar | Confirma equivalencia `famprod ≡ efamilia` |
| `sucproc` | 16 (MX) | Configuracion de familias por sucursal | **DATOS ACTIVOS** — tabla del Program #138 |
| `equi_famprod` | 12 | Mapeo MAG ↔ BM | Tabla auxiliar de nomenclatura |
| `mlifatipobebida1f` | 32 | Tipo de bebida por familia | Clasificacion de articulo, no produccion |

### Decision de Arquitectura para Odoo 19

Basandose en estos hallazgos, se decidio **crear el modelo `bm.ctl.produccion.familia` como entidad independiente con FK a categoria.linea**:

1. **Modelo independiente (no `_inherits`)**: `sucproc` no comparte PK con `mfameq1f` — tiene su propia PK `(compania, sucursal, efamilia)` y sus propios campos de auditoria. Es una entidad distinta que referencia a categoria.linea via FK. El modelo usa Many2one a `bm.ctl.produccion.categoria.linea`.

2. **Solo 2 campos de negocio**: La tabla `sucproc` es minimalista — solo relaciona sucursal con categoria y tiene un campo de estado (activo/inactivo). El modelo refleja esta simplicidad con `sucursal_id`, `categoria_linea_id` y `activo`.

3. **Company implicito**: `company_id` con default `self.env.company` para multi-compania.

4. **Vista lista editable inline**: `editable="bottom"` permite activar/desactivar familias rapidamente sin abrir formularios individuales.

5. **Datos seed replican `sucproc`**: 16 registros iniciales (4 sucursales × 4 familias) con `noupdate="1"` para que el usuario pueda modificar sin sobrescritura.

6. **Compatibilidad con formato legacy**: Se mantienen los campos de auditoria en formato juliano (`feccrea` + 730000) y hora `HHMMSS`.

7. **Menu en Configuraciones**: Ruta `Mantenimiento → Configuraciones → Familia de Produccion` (sequence 10).

### Implementacion del Agente

```
Implementation complete. Created Program #138 "Familia de Produccion" with:
Models (1 file in models/):
- program_138_familia.py - Configuracion de familias de produccion por sucursal
Views (1 file in views/):
- program_138_familia_views.xml - List, form, search views + window action
Data (1 file in data/):
- program_138_familia_data.xml - 16 registros seed (4 sucursales × 4 familias)
Menu updates:
- mantenimiento_configuracion.xml: menu Familia de Produccion con action real (sequence 10)
Security: security/ir.model.access.csv con permisos totales para base.group_user
Updated: __manifest__.py, models/__init__.py
```

### Resumen Digerible: "Encender y apagar lineas de produccion por planta"

1. **Lo que hacia el sistema legacy**: En Big Magic existia una pantalla en `Mantenimiento → Configuraciones → Familia de Produccion` que permitia activar o desactivar categorias de lineas de produccion por sucursal. Por ejemplo: la sucursal 0001 tiene activas las lineas de Envasado (001), Jarabes (003), Maquila (019) y Reempaques (021). Si la sucursal 0070 no produce maquila este mes, se desactiva esa familia ahi. La tabla `sucproc` guardaba 16 combinaciones sucursal-familia, todas activas, con auditoria de quien la creo y cuando.

2. **Lo que estamos haciendo en `models.py`**: Migramos esa configuracion como un modelo simple `bm.ctl.produccion.familia` con tres campos operativos: sucursal (extraido del catalogo `bm.sucursal`), categoria de linea (extraido de `bm.ctl.produccion.categoria.linea` del Program #137), y un switch de activo/inactivo. El nombre se genera automaticamente como "0001 / 001".

3. **Las 4 categorias activas son el corazon de la produccion**: De las 27 categorias del Program #137, solo 4 estan configuradas en `sucproc` para las 4 sucursales operativas:
    - *001 EQUIPOS DE ENVASADO*: Llenadoras de botellas y latas. La mas operativa.
    - *003 TANQUES DE JARABE*: Mezclado y preparacion de jarabes terminados.
    - *019 MAQUILA*: Produccion para terceros bajo contrato.
    - *021 REEMPAQUES*: Re-empaque de producto terminado.
    
    Las otras 11 categorias activas del catalogo #137 (Soplado, Agua, Bases, Azucar, Ploteo, Etiquetas, Termoencogible, Botella, Exhibidores, Snacks) no estan en `sucproc` porque son **lineas auxiliares/intermedias** — su activacion se maneja implicitamente o desde otros modulos.

4. **Relacion Program #137 ↔ #138**: El #137 es "que categorias existen" (catalogo), el #138 es "cuales estan prendidas en cada planta" (configuracion). Son dos caras de la misma moneda. El primero se accede desde Clasificadores, el segundo desde Configuraciones — ambos en Mantenimiento.

5. **Odoo pone el orden**: La lista editable permite al supervisor de produccion activar o desactivar familias por sucursal con un solo clic. Los filtros de activos/inactivos y la agrupacion por sucursal o categoria facilitan ver rapidamente que plantas estan operando que tipos de lineas.

### Detalle de los Scripts

#### `program_138_familia.py` - El modelo de configuracion

Este archivo define el modelo `bm.ctl.produccion.familia` que configura que categorias de lineas de produccion operan en cada sucursal.

**Estructura del modelo:**
- `_name = 'bm.ctl.produccion.familia'`: Nombre tecnico del modelo en el ORM de Odoo
- `_description`: Descripcion legible: "Familia de Produccion por Sucursal (Program 138)"
- `_order = 'sucursal_id, categoria_linea_id'`: Ordenamiento por defecto por sucursal, luego categoria

**Campos operativos:**
- `sucursal_id` (Many2one → `bm.sucursal`, required, ondelete='restrict'): Referencia a la sucursal operativa. Las 4 sucursales activas son 0001, 0068, 0070, 0108. `ondelete='restrict'` evita borrar una sucursal si tiene familias configuradas.
- `categoria_linea_id` (Many2one → `bm.ctl.produccion.categoria.linea`, required, ondelete='restrict'): Referencia a la categoria de linea de produccion. Vincula esta configuracion con el catalogo del Program #137. `ondelete='restrict'` protege contra borrado accidental de categorias en uso.
- `activo` (Boolean, default=True): Switch de activacion. Mapea el campo `estado = 'A'`/'I' del legacy. Permite desactivar familias sin borrarlas.
- `company_id` (Many2one → `res.company`, default=lambda self: self.env.company): Compania propietaria del registro. Se asigna automaticamente al crear.

**Campo computado:**
- `name` (Char, compute='_compute_name', store=True): Nombre legible generado automaticamente como `{sucursal.codigo} / {categoria.efamilia}`. Ejemplo: "0001 / 001", "0068 / 019". Depende de `sucursal_id.codigo` y `categoria_linea_id.efamilia`. Se almacena (`store=True`) para busquedas y ordenamiento.

**Campos de auditoria (compatibilidad legacy):**
- `feccrea` (Integer, required): Fecha de creacion en formato juliano. Calculo: `(dias_desde_1_ene_del_anio) + 730000`.
- `horcrea` (Char, required): Hora de creacion en formato `HHMMSS`.
- `usucrea` (Char, required): Login del usuario creador. Se obtiene de `self.env.user.login`.
- `fecultmod` (Integer): Fecha de ultima modificacion en juliano.
- `horultmod` (Char): Hora de ultima modificacion.
- `usuaulmod` (Char): Login del ultimo usuario modificador.

**Metodos clave:**

1. `_default_fecha()` (decorado con `@api.model`):
```python
def _default_fecha(self):
    today = date.today()
    base = date(today.year, 1, 1)
    return (today - base).days + 730000
```
Calcula el dia juliano: dias desde el 1 de enero del año actual + offset 730000.

2. `_compute_name()` (decorado con `@api.depends('sucursal_id.codigo', 'categoria_linea_id.efamilia')`):
```python
def _compute_name(self):
    for rec in self:
        codigo = rec.sucursal_id.codigo or ''
        efamilia = rec.categoria_linea_id.efamilia or ''
        if codigo and efamilia:
            rec.name = f'{codigo} / {efamilia}'
        else:
            rec.name = ''
```
Genera el nombre compuesto sucursal/categoria. Si alguno falta, deja el nombre vacio temporalmente.

3. `create()` (override con `@api.model_create_multi`):
```python
def create(self, vals_list):
    for vals in vals_list:
        if not vals.get('usucrea'):
            vals['usucrea'] = self.env.user.login
        if not vals.get('feccrea'):
            vals['feccrea'] = self._default_fecha()
        if not vals.get('horcrea'):
            vals['horcrea'] = fields.Datetime.now().strftime('%H%M%S')
    return super().create(vals_list)
```
Intercepta la creacion para poblar automaticamente los campos de auditoria. Respeta valores ya especificados (ej: durante migracion desde el legacy).

4. `write()` (override):
```python
def write(self, vals):
    if not vals.get('usuaulmod'):
        vals['usuaulmod'] = self.env.user.login
    if not vals.get('fecultmod'):
        vals['fecultmod'] = self._default_fecha()
    if not vals.get('horultmod'):
        vals['horultmod'] = fields.Datetime.now().strftime('%H%M%S')
    return super().write(vals)
```
Actualiza los campos de ultima modificacion en cada escritura.

#### `program_138_familia_views.xml` - Las vistas

**List View (editable="bottom"):**
```xml
<list string="Familias de Produccion por Sucursal" editable="bottom">
    <field name="sucursal_id"/>
    <field name="categoria_linea_id"/>
    <field name="activo"/>
</list>
```
- `editable="bottom"`: Permite crear y editar registros directamente en la lista. Ideal para activar/desactivar familias rapidamente.
- Solo 3 campos visibles: sucursal, categoria y switch de activo. Minimalista e intuitivo.
- Los campos de auditoria NO aparecen en la lista (se llenan automaticamente).

**Form View:**
```xml
<form string="Familia de Produccion" edit="true">
    <sheet>
        <div class="oe_title">
            <h1><field name="name" readonly="1"/></h1>
        </div>
        <group>
            <group string="Configuracion">
                <field name="sucursal_id"/>
                <field name="categoria_linea_id"/>
                <field name="activo"/>
            </group>
            <group string="Auditoria">
                <field name="feccrea" readonly="1"/>
                <field name="horcrea" readonly="1"/>
                <field name="usucrea" readonly="1"/>
                <field name="fecultmod" readonly="1"/>
                <field name="horultmod" readonly="1"/>
                <field name="usuaulmod" readonly="1"/>
            </group>
        </group>
    </sheet>
</form>
```
- `oe_title` con `name` readonly: Muestra el nombre computado ("0001 / 001") como titulo.
- Dos grupos logicos: Configuracion (editable) y Auditoria (solo lectura).

**Search View:**
```xml
<search string="Buscar Familias de Produccion">
    <field name="sucursal_id"/>
    <field name="categoria_linea_id"/>
    <separator/>
    <filter name="activos" string="Activos" domain="[('activo', '=', True)]"/>
    <filter name="inactivos" string="Inactivos" domain="[('activo', '=', False)]"/>
    <group>
        <filter name="grupo_sucursal" string="Sucursal" context="{'group_by': 'sucursal_id'}"/>
        <filter name="grupo_categoria" string="Categoria" context="{'group_by': 'categoria_linea_id'}"/>
    </group>
</search>
```
- **Autocomplete**: Busqueda por sucursal y categoria.
- **Filtros rapidos**: Activos/Inactivos.
- **Agrupacion**: Por sucursal o por categoria para analisis operativo.

**Window Action:**
```xml
<record id="action_familia" model="ir.actions.act_window">
    <field name="name">Familias de Produccion</field>
    <field name="res_model">bm.ctl.produccion.familia</field>
    <field name="view_mode">list,form</field>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">
            Configura las familias de produccion por sucursal
        </p>
        <p>
            Activa o desactiva las categorias de lineas de produccion para cada sucursal operativa.
        </p>
    </field>
</record>
```
- `view_mode="list,form"`: Lista como vista default.
- `help`: Mensaje cuando la lista esta vacia (antes de cargar datos seed).

**Menu en Mantenimiento:**
```xml
<menuitem id="menu_familia_produccion"
          name="Familia de Produccion"
          parent="mant_configuraciones_menu"
          action="action_familia"
          sequence="10"/>
```
- `parent="mant_configuraciones_menu"`: Se ubica bajo Configuraciones de Mantenimiento.
- `sequence="10"`: Primer item del menu de Configuraciones.
- Ruta completa: `Mantenimiento → Configuraciones → Familia de Produccion`

#### `program_138_familia_data.xml` - Datos iniciales

Archivo seed con `noupdate="1"` que carga las 16 configuraciones del legacy `sucproc` al instalar el modulo:

**Sucursal 0001 — 4 familias:**
- `001` EQUIPOS DE ENVASADO (categoria_001)
- `003` TANQUES DE JARABE (categoria_003)
- `019` MAQUILA (categoria_019)
- `021` REEMPAQUES (categoria_021)

**Sucursal 0068 — 4 familias (identicas a 0001)**

**Sucursal 0070 — 4 familias (identicas a 0001)**

**Sucursal 0108 — 4 familias (identicas a 0001)**

**Notas sobre los datos seed:**
- `noupdate="1"`: Una vez cargados, los usuarios pueden modificar activaciones sin que las actualizaciones del modulo las sobrescriban.
- Las 4 sucursales comparten exactamente las mismas 4 familias activas (16 registros = 4 × 4).
- Si una sucursal nueva necesita configuracion, se crea manualmente desde la UI.
- Las referencias `categoria_001`, `categoria_003`, etc. apuntan a los External IDs definidos en `program_137_categoria_linea_data.xml`.

#### `ir.model.access.csv` - Seguridad

```csv
access_bm_ctl_produccion_familia,bm.ctl.produccion.familia,model_bm_ctl_produccion_familia,base.group_user,1,1,1,1
```
- `model_id:id`: `model_bm_ctl_produccion_familia` — external ID automatico de Odoo.
- `group_id:id`: `base.group_user` = todos los usuarios internos.
- `perm_read,perm_write,perm_create,perm_unlink`: 1,1,1,1 (acceso total).

#### `models/__init__.py` - Orden de carga

```python
# program 137 - catalogo de categorias de lineas de produccion
from . import program_137_categoria_linea
# sucursal
from . import sucursal
# program 138 - familia de produccion por sucursal
from . import program_138_familia
```
- `program_137_categoria_linea` y `sucursal` deben cargarse **antes** que `program_138_familia` porque este tiene Many2one a ambos.

#### `__manifest__.py` - Orden de carga de archivos XML

```python
'views/program_137_categoria_linea.xml',       # define action_categoria_linea y External IDs de datos
'views/sucursal_views.xml',                    # define action_sucursal y External IDs de datos
'views/program_138_familia_views.xml',          # define action_familia
...
'views/mantenimiento_configuracion.xml',        # referencia action_familia (debe cargarse despues)
...
'data/program_137_categoria_linea_data.xml',   # External IDs para categoria_001, etc.
'data/sucursal_data.xml',                      # External IDs para sucursal_0001, etc.
'data/program_138_familia_data.xml',           # depende de los External IDs anteriores
```
- Las vistas que definen acciones deben cargarse **antes** que los menus que las referencian.
- Los datos seed deben cargarse en orden de dependencia: categorias y sucursales primero, familias despues.

### Integracion Futura

Este modelo es la **configuracion base** para los siguientes modulos:

1. **Validacion de lineas por sucursal**: Cuando se implemente el modelo `bm.ctl.produccion.linea`, cada linea fisica de produccion tendra una sucursal y una categoria. El modelo `familia` permitira validar que una linea solo pueda crearse si su combinacion (sucursal, categoria) esta activa.

2. **Planificacion de produccion (DRP)**: La tabla `drplinpro` (vacia para MX) muestra que el legacy tenia previsto usar la configuracion de familias por sucursal para planificar capacidad. En Odoo, esto se implementara como restriccion en el modulo de planificacion.

3. **Reportes de capacidad por sucursal**: Al cruzar `familia` con `caplinea` (lineas fisicas), se podra generar un reporte de "cuantas lineas tiene cada sucursal por categoria" y "cual es la capacidad instalada por categoria en cada planta".

4. **Control de acceso por sucursal**: El modelo `familia` puede servir como base para restringir que usuarios de una sucursal solo vean/configuran lineas de las categorias activas en su planta.

5. **Activacion/desactivacion masiva**: Un wizard que permita copiar la configuracion de una sucursal a otra, o activar/desactivar todas las categorias de una sucursal de una vez (ej: al abrir una nueva planta o al cerrar temporalmente una existente).

6. **Auditoria de cambios**: Reporte historico de que supervisor activo/desactivo que categoria en que sucursal y cuando. Util para analisis de capacidad operativa historica.

7. **Conexion con Paradas y Mermas**: Cuando se registren paradas o mermas, validar que la combinacion sucursal-categoria este activa en `familia`, evitando registros huerfanos.
