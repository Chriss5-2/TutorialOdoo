## Analisis Post-Implementacion - Program #133 (Paradas)

### Contexto de Validacion
El agente ejecuto 12+ consultas SQL exhaustivas contra la base de datos legacy `mxbdaje_local` para rastrear cualquier evidencia de catalogos de paradas. Revisar [validacion_program_133.md](data_para_agente/validaciones_programs/validacion_program_133.md) para el detalle completo de cada query.

### Logica de Validacion y Hallazgos Tecnicos
La validacion se realizo mediante un proceso de descarte sistematico en cuatro etapas, lo que confirmo que **no existe implementacion operativa** de paradas en el sistema legacy de Mexico:

1. **Busqueda de tablas maestras de paradas**: Se ejecutaron consultas buscando patrones `b*1f` y `m*1f` (siguiendo el patron de `bturno1f` para turnos), busquedas por nombre (`%parada%`, `%paro%`, `%downtime%`), y busquedas por columnas (`%parada%`, `%paro%`, `%motivo%`, `%causa%`).
    - Resultado: **0 tablas maestras de tipos de paradas encontradas**. La unica tabla relacionada es `agrparoee` (paros OEE), pero esta completamente vacia.
    - Conclusion: El catalogo de tipos de paradas **nunca se creo** en el sistema legacy.

2. **Auditoria de tablas OEE (`agrupoe`, `agrupoe1`, `agrparoee`)**: Se inspecciono la estructura DDL y el contenido de las tres tablas diseñadas para clasificacion jerarquica de paradas OEE.
    - `agrupoe` (grupos globales): 0 registros
    - `agrupoe1` (subgrupos detalle): 0 registros
    - `agrparoee` (paros especificos): 0 registros
    - Interpretacion: La estructura fue diseñada (tiene indices, columnas, relaciones) pero **nunca se populo operativamente**. Es una estructura huérfana.

3. **Rastreo de campos en tablas transaccionales**: Se auditaron tablas de produccion (`tpro*`, `opx*`, `prgopdet`) buscando campos de paradas, tiempos muertos o duracion.
    - Hallazgo: `prgopdet.asigparada` es un campo **boolean** (True/False), no una referencia a un tipo de parada. Solo indica si una OP tiene paradas asignadas, pero no dice de que tipo.
    - En tablas `tpro*` y `opx*`: **0 campos** relacionados con paradas, tiempos muertos o duracion.
    - Interpretacion: El sistema legacy no registra el tipo de parada, solo un flag binario. No hay trazabilidad de causa.

4. **Verificacion de logica embebida (triggers, stored procedures, vistas)**: Se audito `information_schema.triggers`, `information_schema.routines` y `information_schema.views` buscando logica relacionada con paradas u OEE.
    - Resultado: **0 triggers**, **0 stored procedures**, **0 vistas** relacionadas con paradas.
    - Los 5 triggers encontrados en `tprolt1f` son de contabilidad (letras/cargos), no de produccion.
    - Interpretacion: No hay logica oculta que deba replicarse. La implementacion en Odoo 19 sera limpia.

### Tabla Resumen de Hallazgos Legacy

| Tabla | Registros | Proposito Esperado | Estado Real |
|---|---|---|---|
| `agrparoee` | 0 | Catalogo de paros OEE | Estructura vacia, nunca se uso |
| `agrupoe` | 0 | Grupos de paradas (global) | Estructura vacia |
| `agrupoe1` | 0 | Subgrupos de paradas (detalle) | Estructura vacia |
| `mtiempoi1f` | 0 | Tiempos improductivos | Vacía + no aplica (es de embarque) |
| `prgopdet` | 53,259 | Programacion OP con flag `asigparada` | Solo flag boolean, sin tipos |
| `bmotiv1f` | 3,215 | Motivos contables/financieros | No aplica a paradas de produccion |
| `bproce1f` | 3,680 | Procedimientos contables/logisticos | No aplica a paradas |
| `vsbtiempo` | Miles | Tabla calendario (DW) | No aplica, es dimension de tiempo |

### Decision de Arquitectura para Odoo 19
Basandose en estos hallazgos, se decidio **crear desde cero** en lugar de intentar migrar estructuras vacias:

1. **Modelo limpio sin deuda tecnica**: Las tablas legacy tienen estructuras incompletas (sin datos, sin triggers, sin logica). Crear desde cero permite diseñar un modelo optimizado para las necesidades reales de Mexico.
2. **Categorias globales estandarizadas**: Se definen 7 categorias que cubren todos los escenarios de paradas en planta: Mecanica, Electrica, Operativa, Calidad, Falta de Material, Mantenimiento, Otros.
3. **Compatibilidad con formato legacy**: Se mantienen los campos de auditoria en formato juliano (`feccrea` + 730000) y hora `HHMMSS` para que los reportes que salgan de Odoo puedan ser leidos por sistemas legacy si es necesario.
4. **Vista editable inline**: Se usa `editable="bottom"` para permitir creacion rapida de tipos de paradas sin abrir formularios individuales, consistente con el patron de Program #132 (Turnos).

### Implementacion del Agente

```
Implementation complete. Created Program#133 "Tipos de Paradas" with:
Models (1 file in models/):
- program_133_paradas.py - Catalogo de tipos de paradas
Views (views/program_133_paradas.xml):
- List view (editable="bottom") con 7 campos operativos
- Form view con 3 grupos (Informacion, Configuracion, Auditoria)
- Window action "Tipos de Paradas"
- Menu item bajo mant_clasificadores_menu (sequence 20)
Security: security/ir.model.access.csv con permisos totales para base.group_user
Updated: __manifest__.py, __init__.py, mantenimiento_clasificadores.xml (removido placeholder)
```

### Resumen Digerible: "Construir el catalogo que nunca existio"

1. **Lo que hacia el sistema legacy**: No hacia nada. Las tablas existian como esqueletos vacios. En `prgopdet` solo habia un checkbox (`asigparada`) que decia "esta OP tiene paradas" pero no decia **que tipo** de parada, **cuanto duró**, ni **por que paso**. Era como tener un registro de asistencia que solo dice "falto alguien" sin decir quien ni por que.

2. **Lo que estamos haciendo en `models.py`**: Estamos construyendo el catalogo completo desde cero. Cada tipo de parada tendra un codigo unico (ej: `MEC001`), una descripcion clara, una categoria, un tiempo estimado y un flag de si afecta el OEE. Odoo registrara automaticamente **quien creo el registro, cuando y a que hora**.

3. **Las 7 categorias cubren todo**: En una planta de bebidas, las paradas siempre caen en una de estas categorias:
    - **MEC** (Mecanica): Se rompio una banda, un motor, una valvula
    - **ELE** (Electrica): Se fue la luz, fallo un sensor, el PLC se colgo
    - **OPE** (Operativa): Hay que cambiar de formato, limpiar la linea, ajustar la maquina
    - **CAL** (Calidad): El producto salio mal, hay que rechazar lote
    - **MAT** (Material): Se acabo el jarabe, faltan envases, no hay etiquetas
    - **MAN** (Mantenimiento): Parada programada para mantenimiento preventivo o correctivo
    - **OTR** (Otros): Cualquier cosa que no encaje en las anteriores

4. **Odoo pone el orden**: A partir de ahora, cada tipo de parada estara documentado, con su tiempo estimado y su impacto en el OEE. Cuando se implemente el modulo de registro de paradas en lineas de produccion, este catalogo sera la base.

### Detalle de los Scripts

#### `program_133_paradas.py` - El modelo principal

Este archivo define el modelo `bm.ctl.produccion.parada` que representa el catalogo de tipos de paradas.

**Estructura del modelo:**
- `_name = 'bm.ctl.produccion.parada'`: Nombre tecnico del modelo en el ORM de Odoo
- `_description`: Descripcion legible que aparece en la UI
- `_order = 'categoria_global, codigo'`: Ordenamiento por defecto (primero por categoria, luego por codigo)

**Campos operativos:**
- `codigo` (Char, required): Codigo unico del tipo de parada. Ejemplo: `MEC001`, `ELE002`, `OPE001`. Este es el identificador principal que se usara en reportes y vinculos futuros.
- `descripcion` (Char, required): Descripcion legible. Ejemplo: "Falla de banda transportadora", "Cambio de formato a 2L".
- `categoria_global` (Selection, required, default='OTR'): Clasificacion macro con 7 opciones. Cada opcion tiene un codigo corto (MEC, ELE, OPE, CAL, MAT, MAN, OTR) y una descripcion larga que aparece en el dropdown.
- `codigo_detalle` (Char, opcional): Subclasificacion para mayor granularidad. Ejemplo: si la categoria es MEC, el detalle podria ser "BANDA", "MOTOR", "SENSOR", "VALVULA".
- `activo` (Boolean, default=True): Permite desactivar tipos de parada que ya no se usan sin borrarlos (importante para mantener integridad historica).
- `tiempo_estimado` (Float): Duracion estimada en minutos. Util para planeacion y calculo de eficiencia. Ejemplo: un cambio de formato podria estimarse en 45 minutos.
- `afecta_oee` (Boolean, default=True): Flag que indica si esta parada impacta el calculo de OEE. Algunas paradas planificadas (como mantenimiento preventivo) podrian no afectar el OEE dependiendo de la politica de la planta.

**Campos de auditoria (compatibilidad legacy):**
- `feccrea` (Integer, required): Fecha de creacion en formato juliano. Se calcula como `(dias_desde_1_ene_del_anio) + 730000`. El offset 730000 es estandar en sistemas AS/400/ERP legacy para mantener compatibilidad.
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
Campo computado que genera un nombre legible combinando codigo y descripcion. Ejemplo: "MEC001 - Falla de banda transportadora". Se almacena (`store=True`) para permitir busquedas y ordenamiento.

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
Intercepta la creacion de registros para asegurar que los campos de auditoria se llenen automaticamente. Usa `model_create_multi` para soportar creacion masiva (varios registros a la vez).

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

#### `program_133_paradas.xml` - Las vistas

**List View (editable="bottom"):**
```xml
<list string="Catalogo de Tipos de Paradas" editable="bottom">
    <field name="codigo"/>
    <field name="descripcion"/>
    <field name="categoria_global"/>
    <field name="codigo_detalle"/>
    <field name="activo"/>
    <field name="tiempo_estimado"/>
    <field name="afecta_oee"/>
</list>
```
- `editable="bottom"`: Permite crear y editar registros directamente en la lista sin abrir formulario. Las nuevas filas se agregan al final.
- Orden de campos: De izquierda a derecha, de mas importante a menos. El codigo y descripcion son los identificadores principales, la categoria es el clasificador, y los ultimos campos son configuracion.
- Los campos de auditoria NO aparecen en la lista (son de solo lectura y se llenan automaticamente).

**Form View:**
```xml
<form string="Definicion de Tipo de Parada" edit="true">
    <sheet>
        <div class="oe_title">
            <h1><field name="name" readonly="1"/></h1>
        </div>
        <group>
            <group string="Informacion de Parada">
                <field name="codigo"/>
                <field name="descripcion"/>
                <field name="categoria_global"/>
                <field name="codigo_detalle"/>
                <field name="activo"/>
            </group>
            <group string="Configuracion">
                <field name="tiempo_estimado"/>
                <field name="afecta_oee"/>
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
- `edit="true"`: Permite edicion directa en el formulario.
- `oe_title` con `name` en `readonly`: Muestra el nombre computado como titulo principal, pero no permite editarlo manualmente (se genera automaticamente).
- Tres grupos organizados logicamente: Informacion (datos principales), Configuracion (parametros operativos), Auditoria (trazabilidad, todos readonly).

**Window Action:**
```xml
<record id="action_parada_definicion" model="ir.actions.act_window">
    <field name="name">Tipos de Paradas</field>
    <field name="res_model">bm.ctl.produccion.parada</field>
    <field name="view_mode">list,form</field>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">
            Crea el catalogo de tipos de paradas de produccion
        </p>
        <p>
            Define los tipos de paradas (mecanica, electrica, operativa, etc.) para registro de tiempos muertos y calculo de OEE.
        </p>
    </field>
</record>
```
- `view_mode="list,form"`: La vista lista es la default, el formulario se abre al hacer clic en un registro.
- `help`: Mensaje que aparece cuando no hay registros (pantalla vacia con cara sonriente).

**Menu Item:**
```xml
<menuitem id="menu_catalogo_paradas"
          name="Paradas"
          parent="mant_clasificadores_menu"
          action="action_parada_definicion"
          sequence="20"/>
```
- `parent="mant_clasificadores_menu"`: Se ubica bajo el menu Clasificadores de Mantenimiento.
- `sequence="20"`: Aparece despues de Turnos (sequence 10), antes de Mermas (sequence 30).
- Ruta completa en la UI: `Mantenimiento → Clasificadores → Paradas`

#### `ir.model.access.csv` - Seguridad

```csv
access_bm_ctl_produccion_parada,bm.ctl.produccion.parada,model_bm_ctl_produccion_parada,base.group_user,1,1,1,1
```
- `model_id:id`: `model_bm_ctl_produccion_parada` es el external ID que Odoo genera automaticamente para el modelo (prefijo `model_` + nombre del modelo con puntos reemplazados por guiones bajos).
- `group_id:id`: `base.group_user` = todos los usuarios internos de Odoo.
- `perm_read,perm_write,perm_create,perm_unlink`: Todos en 1 (acceso total).

#### `__init__.py` - Orden de carga

```python
# program 133 - catalogo de tipos de paradas de produccion
from . import program_133_paradas
```
Se agrega al final del archivo, despues de los imports de Program #132. El orden no es critico aqui porque este modelo no tiene relaciones Many2one con otros modelos del modulo (es un catalogo independiente).

#### `__manifest__.py` - Registro del modulo

```python
'views/program_133_paradas.xml',
```
Se agrega la vista al final de la lista de datos, despues de `program_162_formula_aprobacion.xml`. El orden de carga de vistas no es critico porque no hay dependencias entre ellas.

#### `mantenimiento_clasificadores.xml` - Limpieza

Se elimino el menu placeholder que apuntaba a `base.action_partner_form` (accion incorrecta de partners):
```xml
<!-- ANTES (eliminado) -->
<menuitem id="menu_mantenimiento_paradas"
          name="Paradas"
          parent="mant_clasificadores_menu"
          action="base.action_partner_form"
          sequence="20"/>
```
El menu real se define en `program_133_paradas.xml` con la accion correcta.

### Datos Iniciales Sugeridos (17 tipos estandarizados)

Estos son los tipos de parada recomendados para cargar inicialmente en el sistema:

| Codigo | Descripcion | Categoria | Detalle | Tiempo Est. | Afecta OEE |
|---|---|---|---|---|---|
| MEC001 | Falla de banda transportadora | MEC | BANDA | 30 min | Si |
| MEC002 | Falla de motor principal | MEC | MOTOR | 60 min | Si |
| MEC003 | Falla de sensor/proximidad | MEC | SENSOR | 15 min | Si |
| MEC004 | Falla de valvula/neumatica | MEC | VALVULA | 20 min | Si |
| ELE001 | Falla de PLC/controlador | ELE | PLC | 45 min | Si |
| ELE002 | Falla de tablero electrico | ELE | TABLERO | 30 min | Si |
| OPE001 | Cambio de formato/tamaño | OPE | FORMATO | 45 min | Si |
| OPE002 | Limpieza de linea | OPE | LIMPIEZA | 30 min | Si |
| OPE003 | Ajuste de maquina/calibracion | OPE | AJUSTE | 20 min | Si |
| CAL001 | Rechazo de producto/lote | CAL | RECHAZO | Variable | Si |
| CAL002 | Ajuste de parametros de calidad | CAL | AJUSTE | 15 min | Si |
| MAT001 | Falta de jarabe/concentrado | MAT | JARABE | Variable | Si |
| MAT002 | Falta de envases/botellas | MAT | ENVASES | Variable | Si |
| MAT003 | Falta de etiquetas/tapas | MAT | ETIQUETAS | Variable | Si |
| MAN001 | Mantenimiento preventivo | MAN | PREVENTIVO | Segun plan | No |
| MAN002 | Mantenimiento correctivo | MAN | CORRECTIVO | Variable | Si |
| OTR001 | Otros (especificar en descripcion) | OTR | - | Variable | Si |

**Notas sobre los datos sugeridos:**
- Los tiempos estimados son referenciales y deben ajustarse segun la realidad de cada planta.
- Las paradas de "Falta de Material" tienen tiempo variable porque dependen del proveedor y la logistica.
- El mantenimiento preventivo tiene `afecta_oee = No` porque es una parada planificada que no deberia penalizar el indicador de eficiencia.
- El codigo OTR001 es un comodin para paradas que no encajen en las categorias existentes.

### Integracion Futura

Este modelo es la **base fundamental** para los siguientes modulos que se implementaran:

1. **Registro de Paradas en Lineas de Produccion**: Un nuevo modelo que vinculara `bm.ctl.produccion.parada` con `mlinea1f` (lineas de produccion) y `bturno1f` (turnos) para registrar cada parada real con: linea, turno, tipo de parada, hora inicio, hora fin, duracion real, operador que la reporto.

2. **Calculo de OEE (Overall Equipment Effectiveness)**: Usando los tipos de parada y su flag `afecta_oee`, se calculara el OEE real de cada linea:
   - `Disponibilidad = Tiempo Productivo / Tiempo Planificado`
   - Las paradas con `afecta_oee = True` reducen el tiempo productivo
   - Las paradas con `afecta_oee = False` (como mantenimiento preventivo) no penalizan

3. **Reportes de Analisis de Paradas**:
   - Pareto de paradas por categoria (que categorias causan mas tiempo muerto)
   - Analisis por linea (que lineas tienen mas paradas)
   - Analisis por turno (que turnos tienen mas incidencias)
   - Tendencia temporal (evolucion de paradas por mes/semana)

4. **Alertas y Thresholds**: Configurar umbrales de alerta cuando un tipo de parada supera cierta frecuencia o duracion en un periodo determinado.
