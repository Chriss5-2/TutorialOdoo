## Analisis Post-Implementacion - Program #135 (Mermas)

### Contexto de Validacion
El agente ejecuto 15+ consultas SQL exhaustivas contra la base de datos legacy `mxbdaje_local` para rastrear la arquitectura de gestion de mermas, desperdicios y perdidas de produccion. Revisar [validacion_program_135.md](data_para_agente/validaciones_programs/validacion_program_135.md) para el detalle completo de cada query.

### Logica de Validacion y Hallazgos Tecnicos
La validacion se realizo mediante un proceso de descubrimiento sistematico en cinco etapas, lo que confirmo que **existe implementacion parcial** de mermas en el sistema legacy de Mexico:

1. **Busqueda de tablas maestras de mermas**: Se ejecutaron consultas buscando patrones `%merm%`, `%desp%`, `%perd%`, `%waste%`, `%scrap%` en nombres de tablas y columnas.
    - Resultado: **6 tablas encontradas** relacionadas con mermas: `tipmer`, `mermastdmes`, `merppro`, `merxlin`, `mcatppres`, `tproin1`.
    - Hallazgo clave: A diferencia de paradas (donde no existia NADA), aqui SI existe un catalogo (`tipmer`) con 160 registros y una tabla de analisis (`mermastdmes`) con 799,682 registros de Mexico.

2. **Auditoria del catalogo `tipmer`**: Se inspecciono la estructura DDL y el contenido del catalogo de tipos de merma.
    - `tipmer`: 160 registros totales, pero **NINGUNO** para las companias de Mexico (0030, 0035).
    - Companias con datos: 0002 (Peru, 62 tipos), 9100 (53 tipos), 0015 (37 tipos), 0100 (7 tipos), 9999 (1 tipo).
    - Estructura: Tabla plana con `(compania, tipmerma)` como PK, campos de auditoria completos, sin categorizacion jerarquica.
    - Interpretacion: El catalogo existe pero **nunca se configuro para Mexico**. Mexico usaba un enfoque diferente basado en `tipart` (tipo de articulo) y `desfamilia` (familia descriptiva).

3. **Auditoria de `mermastdmes` (tabla de analisis)**: Se inspecciono la tabla principal de datos de mermas.
    - 799,682 registros para Mexico (0030: 718,662, 0035: 81,020).
    - 11 familias de articulo (`tipart`) operativas: 001 (Equipos de Envasado), 003 (Tanques de Jarabe), 005 (Tanques de Agua), 008 (Bases Terminadas), 009 (Bases Intermediarias), 010 (Azucar Liquida), 017 (Unidad de Ploteo), 021 (Reempaque), 025 (Etiquetas), 026 (Termoencogible), 051 (Exhibidores).
    - Campos clave: `qstd` (cantidad estandar), `qreal` (cantidad real), `vstd` (valor estandar), `vreal` (valor real), `pormerma` (porcentaje de merma).
    - Hallazgo critico: `pormerma` NO es calculable como `(qreal - qstd) / qstd * 100`. Los valores son anomalous (935%, 241%, 216%) y no corresponden a la formula estandar. Es un factor acumulado no estandarizado.
    - `nuevovreal`: Campo de valor ajustado/reasignado (posiblemente despues de sustituciones). Cuando `nuevovreal = 0`, `pormerma` es 0 o un valor alto sin relacion directa.
    - `insumochild` + `tipochild = 'SUS'`: Rastrea **sustituciones de insumos** (cuando se uso un insumo diferente al de la receta original). Hallazgo no documentado inicialmente.
    - Duplicados por `(nroop, insumo, fliqui)`: Registros con `count = 2`, indicando ajustes posteriores o re-calculos.
    - Interpretacion: `mermastdmes` es una tabla de **resultado de procesamiento batch** (cierre de mes), no transaccional en tiempo real. Las fechas tienen hora fija `12:59:55`.

4. **Auditoria de tablas transaccionales (`merppro`, `merxlin`, `mcatppres`, `tproin1`)**:
    - `merppro` (mermas por OP): 0 registros. Diseñada para vincular mermas con ordenes de produccion, nunca se opero.
    - `merxlin` (mermas por linea): 0 registros. Diseñada para desglose por linea con campos `qliq`, `qenv`, `qins`, nunca se opero.
    - `mcatppres` (% merma por categoria): 0 registros. Configuracion de porcentajes estandar, nunca se opero.
    - `tproin1` (protocolos con qmerma): 0 registros. Protocolos de control de calidad, nunca se opero.
    - `prgopdet.asigmerma`: 53,259 registros pero **NINGUNO** con `asigmerma = true`. El flag nunca se uso.
    - Interpretacion: Las tablas transaccionales fueron diseñadas pero **nunca se poblaron operativamente**. Mexico solo tiene datos de analisis (`mermastdmes`), no de registro en tiempo real.

5. **Verificacion de logica embebida (triggers, stored procedures, vistas)**:
    - Resultado: **0 triggers**, **0 stored procedures**, **0 vistas** relacionadas con mermas.
    - Interpretacion: No hay logica oculta que deba replicarse. La implementacion en Odoo 19 sera limpia.

### Tabla Resumen de Hallazgos Legacy

| Tabla | Registros | Proposito Esperado | Estado Real |
|---|---|---|---|
| `tipmer` | 160 | Catalogo de tipos de merma | Datos existen pero NO para Mexico (0030, 0035) |
| `mermastdmes` | 799,682 | Analisis merma std vs real por mes | **DATOS ACTIVOS de Mexico**, tabla de resultado batch |
| `merppro` | 0 | Mermas transaccionales por OP | Vacía, nunca se opero |
| `merxlin` | 0 | Mermas por linea de produccion | Vacía, nunca se opero |
| `mcatppres` | 0 | % merma estandar por categoria | Vacía, nunca se opero |
| `tproin1` | 0 | Protocolos con qmerma | Vacía, nunca se opero |
| `prgopdet.asigmerma` | 53,259 (0 con merma) | Flag de merma asignada en OP | Nunca se uso |
| `dethcos` (campos merma) | 45,234 | Costos de merma | Todos los campos de merma en 0 |

### Decision de Arquitectura para Odoo 19
Basandose en estos hallazgos, se decidio **crear desde cero con enfoque hibrido**: aprovechar las 11 familias de `tipart` y los porcentajes de `mermastdmes` como referencia, pero diseñar una estructura adaptada a las necesidades reales de Mexico.

1. **Dos niveles de clasificacion**:
    - `categoria_global` (Selection): Clasificacion macro basada en las familias de `mermastdmes` (LIQ, ENV, INS, ETQ, EMP, CAL, FOR, OTR).
    - `tipart_original` (Char): Codigo `tipart` original del legacy (001-051) para trazabilidad.

2. **Modelo limpio sin deuda tecnica**: Las tablas transaccionales legacy estan vacias. Crear desde cero permite diseñar un modelo optimizado con campos computed para `cantidad_merma`, `porcentaje_merma` y `costo_merma`.

3. **Compatibilidad con formato legacy**: Se mantienen los campos de auditoria en formato juliano (`feccrea` + 730000) y hora `HHMMSS` para compatibilidad con reportes legacy.

4. **Vista editable inline**: Se usa `editable="bottom"` para permitir creacion rapida de tipos de merma y registros transaccionales sin abrir formularios individuales.

5. **Decoracion visual en listas**: Registros con merma >10% en rojo, >5% en naranja para identificacion rapida de desviaciones criticas.

### Implementacion del Agente

```
Implementation complete. Created Program#135 "Mermas" with:

Models (2 files in models/):
- program_135_mermas.py - Catalogo de tipos de mermas
- program_135_merma_registro.py - Registro transaccional de mermas

Views (2 files in views/):
- program_135_mermas.xml - List, form, search views + menu (Mantenimiento)
- program_135_merma_registro.xml - List, form, search views + menu (Produccion)

Data (1 file in data/):
- program_135_merma_data.xml - 22 tipos de merma iniciales

Security: security/ir.model.access.csv con permisos totales para base.group_user
Updated: __manifest__.py, __init__.py, produccion_menu.xml
```

### Resumen Digerible: "Construir lo que existia a medias"

1. **Lo que hacia el sistema legacy**: Tenia un catalogo de mermas para otros paises (Peru, etc.) pero **NO para Mexico**. Mexico tenia 799,682 registros de analisis en `mermastdmes` (comparacion estandar vs real por mes) pero **NINGUN registro transaccional** en tiempo real. Era como tener un reporte mensual de "cuanto se desperdicio" pero sin poder registrar "que se desperdicio hoy y por que". El campo `pormerma` era un factor misterioso que no seguia ninguna formula estandar.

2. **Lo que estamos haciendo en `models.py`**: Estamos construyendo **dos modelos**:
    - **Catalogo (`bm.ctl.produccion.merma`)**: Define los tipos de merma que existen en la planta (Poly Stretch, Etiquetas, Separadores, etc.) con su categoria, porcentaje estandar y si es recuperable.
    - **Registro (`bm.ctl.produccion.merma.registro`)**: Permite registrar mermas reales por orden de produccion, insumo, linea y turno. Calcula automaticamente la cantidad de merma, el porcentaje y el costo.

3. **Las 8 categorias cubren todo**: En una planta de bebidas, las mermas siempre caen en una de estas categorias:
    - **EMP** (Empaque): Poly Stretch, separadores, bolsas, cajas, cinta canela
    - **ETQ** (Etiquetado): Etiquetas RFID, pegamento, film termoencogible
    - **LIQ** (Liquidos): Agua tratada, alta fructosa, azucar liquida, jarabe, bases
    - **INS** (Insumos): Acido citrico, benzoato de sodio, citrato de sodio, gas carbonico
    - **CAL** (Calidad): Merma por pruebas de calidad, rechazo de producto
    - **FOR** (Formato): Merma por cambio de formato/tamaño
    - **OTR** (Otros): Cualquier cosa que no encaje en las anteriores

4. **Odoo pone el orden y el calculo**: A partir de ahora, cada merma se registra con su tipo, cantidad estandar vs real, y Odoo calcula automaticamente el porcentaje y el costo. La lista muestra en **rojo** las mermas >10% y en **naranja** las >5% para identificacion rapida.

### Detalle de los Scripts

#### `program_135_mermas.py` - El modelo de catalogo

Este archivo define el modelo `bm.ctl.produccion.merma` que representa el catalogo de tipos de mermas.

**Estructura del modelo:**
- `_name = 'bm.ctl.produccion.merma'`: Nombre tecnico del modelo en el ORM de Odoo
- `_description`: Descripcion legible que aparece en la UI
- `_order = 'categoria_global, codigo'`: Ordenamiento por defecto (primero por categoria, luego por codigo)

**Campos operativos:**
- `codigo` (Char, required): Codigo unico del tipo de merma. Ejemplo: `EMP001`, `ETQ001`, `LIQ001`. Este es el identificador principal que se usara en reportes y vinculos futuros.
- `descripcion` (Char, required): Descripcion legible. Ejemplo: "Poly Stretch", "Etiqueta TAG RFID", "Agua Tratada para Envasado".
- `categoria_global` (Selection, required, default='OTR'): Clasificacion macro con 8 opciones. Cada opcion tiene un codigo corto (LIQ, ENV, INS, ETQ, EMP, CAL, FOR, OTR) y una descripcion larga que aparece en el dropdown.
- `tipart_original` (Char, opcional): Codigo `tipart` original del sistema legacy (001-051). Permite trazabilidad con los datos historicos de `mermastdmes`.
- `activo` (Boolean, default=True): Permite desactivar tipos de merma que ya no se usan sin borrarlos (importante para mantener integridad historica).
- `porcentaje_estandar` (Float): Porcentaje de merma esperado/permitido. Basado en los promedios historicos de `mermastdmes` (ej: 13.85% para termoencogible, 16.91% para envasado).
- `recuperable` (Boolean, default=False): Indica si la merma es recuperable/reutilizable. Ejemplo: el agua tratada puede ser recuperable, el poly stretch no.
- `afecta_costo` (Boolean, default=True): Indica si la merma impacta el calculo de costos. Algunas mermas (como agua tratada) pueden no afectar el costo directamente.

**Campos de auditoria (compatibilidad legacy):**
- `feccrea` (Integer, required): Fecha de creacion en formato juliano. Se calcula como `(dias_desde_1_ene_del_anio) + 730000`. El offset 730000 es estandar en sistemas AS/400/ERP legacy.
- `horcrea` (Char, required): Hora de creacion en formato `HHMMSS`. Ejemplo: "143022" = 14:30:22.
- `usucrea` (Char, required): Login del usuario que creo el registro. Se obtiene de `self.env.user.login`.
- `fecultmod`, `horultmod`, `usuaulmod`: Equivalentes para ultima modificacion.

**Metodos clave:**

1. `_default_fecha()` (decorado con `@api.model`):
```python
def _default_fecha(self):
    today = date.today()
    base = date(today.year, 1, 1)
    return (today - base).days + 730000
```
Calcula el dia juliano: cuenta los dias desde el 1 de enero del año actual y le suma 730000. Por ejemplo, si hoy es 13 de mayo (dia 133 del año), el resultado es `133 + 730000 = 730133`.

2. `_compute_name()` (decorado con `@api.depends('codigo', 'descripcion')`):
```python
def _compute_name(self):
    for rec in self:
        rec.name = f'{rec.codigo} - {rec.descripcion}' if rec.codigo else rec.descripcion
```
Campo computado que genera un nombre legible combinando codigo y descripcion. Ejemplo: "EMP001 - Poly Stretch". Se almacena (`store=True`) para permitir busquedas y ordenamiento.

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
Intercepta la creacion de registros para asegurar que los campos de auditoria se llenen automaticamente. Usa `model_create_multi` para soportar creacion masiva.

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
Intercepta las modificaciones para actualizar automaticamente los campos de ultima modificacion.

5. `action_save_and_close()`:
```python
def action_save_and_close(self):
    self.ensure_one()
    return {'type': 'ir.actions.act_window_close'}
```
Accion para cerrar la vista desde un boton. Usa `ensure_one()` para garantizar que se ejecuta sobre un solo registro.

#### `program_135_merma_registro.py` - El modelo transaccional

Este archivo define el modelo `bm.ctl.produccion.merma.registro` que permite registrar mermas reales por orden de produccion.

**Estructura del modelo:**
- `_name = 'bm.ctl.produccion.merma.registro'`: Nombre tecnico del modelo
- `_description`: Descripcion legible
- `_order = 'fecha desc, id desc'`: Ordenamiento por defecto (mas recientes primero)

**Campos operativos:**
- `nroop` (Char, required): Numero de orden de produccion asociada. Es Char (no Many2one) porque el modulo `mrp` no esta instalado en la instancia.
- `tipo_merma_id` (Many2one a `bm.ctl.produccion.merma`, required): Referencia al catalogo de tipos de merma.
- `insumo_codigo` (Integer, required): Codigo del insumo que genero la merma. Es Integer (no Many2one a product) porque el modulo `product` no esta instalado.
- `insumo_descripcion` (Char, opcional): Descripcion del insumo para referencia.
- `linea` (Char, opcional): Linea de produccion donde ocurrio la merma.
- `turno` (Char, opcional): Turno donde ocurrio la merma.
- `fecha` (Date, required, default=context_today): Fecha del registro.

**Campos de cantidades:**
- `cantidad_std` (Float, required, default=0.0): Cantidad estandar segun receta. Usa digits 'Product Unit of Measure'.
- `cantidad_real` (Float, required, default=0.0): Cantidad real consumida. Usa digits 'Product Unit of Measure'.
- `cantidad_merma` (Float, computed, store=True): `cantidad_real - cantidad_std`. Se calcula automaticamente.
- `porcentaje_merma` (Float, computed, store=True): `(cantidad_merma / cantidad_std) * 100`. Se calcula automaticamente. Si `cantidad_std = 0`, el porcentaje es 0.

**Campos de costos:**
- `costo_estandar` (Float, default=0.0): Costo estandar unitario del insumo. Se ingresa manualmente (podria automatizarse si se instala el modulo `product`).
- `costo_merma` (Float, computed, store=True): `cantidad_merma * costo_estandar`. Se calcula automaticamente.

**Otros campos:**
- `observaciones` (Text, opcional): Causa y detalles de la merma.
- Campos de auditoria: `feccrea`, `horcrea`, `usucrea`, `fecultmod`, `horultmod`, `usuaulmod` (mismo patron que el catalogo).

**Metodos clave:**

1. `_compute_name()`:
```python
def _compute_name(self):
    for rec in self:
        tipo = rec.tipo_merma_id.codigo if rec.tipo_merma_id else 'S/T'
        rec.name = f'{rec.nroop} - {tipo}' if rec.nroop else tipo
```
Genera un nombre legible combinando la OP y el tipo de merma. Ejemplo: "PALP24000001 - EMP001".

2. `_compute_cantidad_merma()`:
```python
def _compute_cantidad_merma(self):
    for rec in self:
        rec.cantidad_merma = rec.cantidad_real - rec.cantidad_std
```
Calcula la diferencia entre cantidad real y estandar.

3. `_compute_porcentaje_merma()`:
```python
def _compute_porcentaje_merma(self):
    for rec in self:
        if rec.cantidad_std != 0:
            rec.porcentaje_merma = (rec.cantidad_merma / rec.cantidad_std) * 100
        else:
            rec.porcentaje_merma = 0.0
```
Calcula el porcentaje de merma. Protege contra division por cero.

4. `_compute_costo_merma()`:
```python
def _compute_costo_merma(self):
    for rec in self:
        rec.costo_merma = rec.cantidad_merma * rec.costo_estandar
```
Calcula el costo total de la merma.

#### `program_135_mermas.xml` - Las vistas del catalogo

**List View (editable="bottom"):**
```xml
<list string="Tipos de Mermas" editable="bottom">
    <field name="codigo"/>
    <field name="descripcion"/>
    <field name="categoria_global"/>
    <field name="tipart_original"/>
    <field name="porcentaje_estandar"/>
    <field name="recuperable"/>
    <field name="afecta_costo"/>
    <field name="activo"/>
</list>
```
- `editable="bottom"`: Permite crear y editar registros directamente en la lista.
- Los campos de auditoria NO aparecen en la lista (son de solo lectura y se llenan automaticamente).

**Form View:**
```xml
<form string="Tipo de Merma">
    <header>
        <button name="action_save_and_close" string="Guardar y Cerrar" type="object" class="btn-primary"/>
    </header>
    <sheet>
        <group>
            <group string="Informacion General">
                <field name="codigo"/>
                <field name="descripcion"/>
                <field name="categoria_global"/>
                <field name="tipart_original"/>
            </group>
            <group string="Configuracion">
                <field name="porcentaje_estandar"/>
                <field name="recuperable"/>
                <field name="afecta_costo"/>
                <field name="activo"/>
            </group>
        </group>
        <group string="Auditoria" groups="base.group_no_one">
            ...
        </group>
    </sheet>
</form>
```
- Tres grupos organizados logicamente: Informacion General, Configuracion, Auditoria (solo visible para administradores con `base.group_no_one`).

**Search View:**
```xml
<search>
    <filter string="Activos" name="activos" domain="[('activo', '=', True)]"/>
    <filter string="Recuperables" name="recuperables" domain="[('recuperable', '=', True)]"/>
    <group>
        <filter string="Categoria" name="group_categoria" context="{'group_by': 'categoria_global'}"/>
    </group>
</search>
```
- Filtros rapidos para activos y recuperables.
- Group by categoria global.

**Window Action:**
```xml
<record id="action_aje_mermas" model="ir.actions.act_window">
    <field name="name">Tipos de Mermas</field>
    <field name="res_model">bm.ctl.produccion.merma</field>
    <field name="view_mode">list,form</field>
    <field name="context">{'default_activo': True}</field>
</record>
```
- `context` con `default_activo: True`: Al crear un nuevo tipo, viene activo por defecto.

**Menu Item:**
```xml
<menuitem id="menu_mantenimiento_mermas"
          name="Mermas"
          parent="mant_clasificadores_menu"
          action="action_aje_mermas"
          sequence="30"/>
```
- Ruta completa en la UI: `Mantenimiento → Clasificadores → Mermas`
- `sequence="30"`: Aparece despues de Paradas (sequence 20).

#### `program_135_merma_registro.xml` - Las vistas del registro transaccional

**List View (editable="bottom" con decoracion):**
```xml
<list string="Registro de Mermas" editable="bottom" 
      decoration-danger="porcentaje_merma > 10" 
      decoration-warning="porcentaje_merma > 5">
    <field name="fecha"/>
    <field name="nroop"/>
    <field name="tipo_merma_id"/>
    <field name="insumo_codigo"/>
    <field name="insumo_descripcion"/>
    <field name="linea"/>
    <field name="turno"/>
    <field name="cantidad_std"/>
    <field name="cantidad_real"/>
    <field name="cantidad_merma"/>
    <field name="porcentaje_merma"/>
    <field name="costo_estandar"/>
    <field name="costo_merma"/>
</list>
```
- `decoration-danger`: Filas con merma >10% se muestran en **rojo**.
- `decoration-warning`: Filas con merma >5% se muestran en **naranja**.
- Permite identificacion visual rapida de desviaciones criticas.

**Form View:**
```xml
<form string="Registro de Merma">
    <sheet>
        <group>
            <group string="Informacion General">
                <field name="fecha"/>
                <field name="nroop"/>
                <field name="tipo_merma_id"/>
                <field name="insumo_codigo"/>
                <field name="insumo_descripcion"/>
                <field name="linea"/>
                <field name="turno"/>
            </group>
            <group string="Cantidades">
                <field name="cantidad_std"/>
                <field name="cantidad_real"/>
                <field name="cantidad_merma"/>
                <field name="porcentaje_merma"/>
            </group>
            <group string="Costos">
                <field name="costo_estandar"/>
                <field name="costo_merma"/>
            </group>
        </group>
        <group string="Observaciones">
            <field name="observaciones" nolabel="1"/>
        </group>
    </sheet>
</form>
```
- Tres grupos principales: Informacion General, Cantidades, Costos.
- Observaciones en un grupo separado sin label para ocupar todo el ancho.

**Search View:**
```xml
<search>
    <filter string="Hoy" name="hoy" domain="[('fecha', '=', context_today())]"/>
    <filter string="Esta Semana" name="semana" domain="[('fecha', '>=', ...)]"/>
    <filter string="Este Mes" name="mes" domain="[('fecha', '>=', ...)]"/>
    <separator/>
    <filter string="Merma Alta (>10%)" name="merma_alta" domain="[('porcentaje_merma', '>', 10)]"/>
    <filter string="Con Costo" name="con_costo" domain="[('costo_merma', '>', 0)]"/>
    <group>
        <filter string="Tipo de Merma" name="group_tipo" context="{'group_by': 'tipo_merma_id'}"/>
        <filter string="OP" name="group_op" context="{'group_by': 'nroop'}"/>
        <filter string="Fecha" name="group_fecha" context="{'group_by': 'fecha'}"/>
    </group>
</search>
```
- Filtros temporales: Hoy, Esta Semana, Este Mes.
- Filtros operativos: Merma Alta (>10%), Con Costo.
- Group by: Tipo de Merma, OP, Fecha.

**Window Action:**
```xml
<record id="action_aje_merma_registro" model="ir.actions.act_window">
    <field name="name">Registro de Mermas</field>
    <field name="res_model">bm.ctl.produccion.merma.registro</field>
    <field name="view_mode">list,form</field>
    <field name="context">{'default_fecha': context_today()}</field>
</record>
```
- `context` con `default_fecha: context_today()`: Al crear un nuevo registro, la fecha viene con hoy por defecto.

**Menu Item:**
```xml
<menuitem id="menu_prod_ingreso_mermas"
          name="Ingreso de Mermas"
          parent="prod_ingParMermas_menu"
          action="action_aje_merma_registro"
          sequence="10"/>
```
- Ruta completa en la UI: `Producción → Ingreso de Paradas y Mermas → Ingreso de Mermas`
- `sequence="10"`: Aparece antes de "Ingreso de Paradas" (sequence 20).

#### `produccion_menu.xml` - Actualizacion del menu de produccion

Se modifico el menu "Ingreso de Paradas y Mermas" para agregar submenus reales:
```xml
<menuitem id="prod_ingParMermas_menu" name="Ingreso de Paradas y Mermas" parent="prod_menu" sequence="40"/>
    <menuitem id="prod_ing_paradas" name="Ingreso de Paradas" parent="prod_ingParMermas_menu" sequence="10" action="action_parada_definicion"/>
    <menuitem id="prod_ing_mermas" name="Ingreso de Mermas" parent="prod_ingParMermas_menu" sequence="20" action="action_aje_merma_registro"/>
```
- Antes tenia `action="base.action_partner_form"` (placeholder incorrecto).
- Ahora tiene dos submenus reales: Ingreso de Paradas y Ingreso de Mermas.

#### `ir.model.access.csv` - Seguridad

```csv
access_bm_ctl_produccion_merma,bm.ctl.produccion.merma,model_bm_ctl_produccion_merma,base.group_user,1,1,1,1
access_bm_ctl_produccion_merma_registro,bm.ctl.produccion.merma.registro,model_bm_ctl_produccion_merma_registro,base.group_user,1,1,1,1
```
- Dos lineas: una para el catalogo, otra para el registro transaccional.
- `group_id:id`: `base.group_user` = todos los usuarios internos de Odoo.
- Permisos totales (read, write, create, unlink) para ambos modelos.

#### `__manifest__.py` - Orden de carga

El orden de carga es **critico** para evitar errores de "External ID not found":
```python
'data': [
    'security/ir.model.access.csv',
    'views/principal_menu.xml',
    'views/program_132_turnos.xml',
    'views/program_133_paradas.xml',
    'views/program_135_mermas.xml',           # Define action_aje_mermas
    'views/program_135_merma_registro.xml',   # Define action_aje_merma_registro
    'views/produccion_menu.xml',              # Referencia ambas actions
    ...
    'data/program_135_merma_data.xml',        # Datos iniciales (al final)
]
```
- Las vistas que definen actions deben cargarse **antes** que los menus que las referencian.
- Los datos iniciales se cargan al final para asegurar que todos los modelos y vistas existan.

#### `program_135_merma_data.xml` - Datos iniciales

22 tipos de merma cargados automaticamente al instalar el modulo, basados en las 11 familias de `tipart` validadas en `mermastdmes`:

| Codigo | Descripcion | Categoria | Tipart | % Estandar | Recuperable |
|---|---|---|---|---|---|
| EMP001 | Poly Stretch | EMP | 026 | 13.85 | No |
| EMP002 | Separador de Carton | EMP | 001 | 16.91 | No |
| EMP003 | Bolsa de Polietileno | EMP | 001 | 16.91 | No |
| EMP004 | Caja Corrugado | EMP | 001 | 16.91 | No |
| EMP005 | Cinta Canela (Empacotecnia) | EMP | 001 | 16.91 | No |
| ETQ001 | Etiqueta TAG RFID | ETQ | 025 | 16.34 | No |
| ETQ002 | Pegamento para Etiquetadora | ETQ | 025 | 16.34 | No |
| ETQ003 | Film Termoencogible 40cm | ETQ | 026 | 13.85 | No |
| ETQ004 | Film Termoencogible 46cm | ETQ | 026 | 13.85 | No |
| LIQ001 | Agua Tratada para Envasado | LIQ | 005 | 0.00 | Si |
| LIQ002 | Alta Fructosa 55 | LIQ | 010 | 241.02 | No |
| LIQ003 | Azucar Liquida | LIQ | 010 | 241.02 | No |
| LIQ004 | Merma de Jarabe | LIQ | 003 | 0.39 | No |
| LIQ005 | Merma de Base Terminada | LIQ | 008 | 4.65 | No |
| LIQ006 | Merma de Base Intermedia | LIQ | 009 | 0.68 | No |
| INS001 | Acido Citrico | INS | 008 | 4.65 | No |
| INS002 | Benzoato de Sodio | INS | 008 | 4.65 | No |
| INS003 | Citrato de Sodio | INS | 008 | 4.65 | No |
| INS004 | Gas Carbonico | INS | 008 | 4.65 | No |
| CAL001 | Merma por Pruebas de Calidad | CAL | - | 0.00 | No |
| FOR001 | Merma por Cambio de Formato | FOR | - | 0.00 | No |
| OTR001 | Otros | OTR | - | 0.00 | No |

**Notas sobre los datos iniciales:**
- Los porcentajes estandar estan basados en los promedios historicos de `mermastdmes` para compania 0030.
- `LIQ001` (Agua Tratada) tiene `recuperable = Si` y `afecta_costo = No` porque el agua puede reciclarse y su costo es marginal.
- `LIQ002` y `LIQ003` (Alta Fructosa y Azucar Liquida) tienen porcentajes altos (241.02%) porque el `pormerma` legacy era un factor acumulado, no un porcentaje puro. Estos valores deben ajustarse segun la realidad operativa.
- Los tipos EMP y ETQ representan el mayor impacto economico ($45.6M en Poly Stretch, $34.5M en Etiquetas).

### Integracion Futura

Este modelo es la **base fundamental** para los siguientes modulos que se implementaran:

1. **Vinculacion con Maestro de Articulos**: Cuando se instale el modulo `product`, los campos `insumo_codigo` y `insumo_descripcion` podran reemplazarse por `insumo_id` (Many2one a `product.product`) para obtener automaticamente la unidad de medida, costo estandar y familia.

2. **Vinculacion con Ordenes de Produccion**: Cuando se instale el modulo `mrp`, el campo `nroop` podra reemplazarse por `nroop_id` (Many2one a `mrp.production`) para vincular mermas directamente con ordenes de produccion y obtener automaticamente la receta estandar.

3. **Vinculacion con Lineas de Produccion**: Cuando se implemente el modelo `bm.ctl.produccion.linea`, el campo `linea` podra reemplazarse por `linea_id` (Many2one) para agrupar mermas por linea de produccion.

4. **Reportes de Analisis de Mermas**:
    - Pareto de mermas por categoria (que categorias causan mayor costo)
    - Analisis por insumo (que insumos generan mas merma)
    - Analisis por OP (que ordenes tienen mayor desviacion)
    - Tendencia temporal (evolucion de mermas por mes/semana)
    - Comparacion vs estandar (porcentaje real vs porcentaje estandar)

5. **Alertas y Thresholds**: Configurar umbrales de alerta cuando un tipo de merma supera el porcentaje estandar configurado en el catalogo.

6. **Integracion con Modulo de Costos**: Los registros de merma seran insumo para el calculo de desviacion de consumo real vs estandar en el modulo de costos de produccion.

7. **Conexion con OEE**: Las mermas por calidad (CAL) podran vincularse con las paradas por calidad para un analisis integral de eficiencia.
