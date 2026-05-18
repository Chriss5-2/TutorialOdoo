## Analisis Post-Implementacion - Program #574 (Configura Procesos Productivos)

### Contexto de Validacion
Se ejecutaron consultas SQL de introspeccion contra `mxbdaje_local` para rastrear la arquitectura de configuracion de procesos productivos, complementadas con busqueda en `aje_docs_simulacion/01_Docs_Oficiales/`. Revisar [validacion_program_574.md](data_para_agente/validaciones_programs/validacion_program_574.md) para el detalle completo de cada query (secciones 1-5) y la resolucion de las 8 dudas post-analisis (seccion 10).

El resultado fue contundente: **el Program #574 nunca se opero en el sistema legacy para Mexico**. La tabla maestra `mproprod1f` esta vacia (0 registros), los Stored Procedures asociados no existen en `mxbdaje_local`, y Mexico (0030) no tiene ninguna configuracion en `ctm_proceso_linea`. Esto representa una oportunidad de "Clean Slate" — diseno desde cero sin deuda tecnica.

### Logica de Validacion y Hallazgos Tecnicos

La validacion se realizo mediante un proceso de **descarte en cinco etapas**, combinando docs oficiales con consultas directas a BD:

1. **Exploracion de documentacion oficial**: Se busco en `01_Docs_Oficiales/` y todas sus subcarpetas referencias al Program #574.
    - Resultado: **0 documentacion funcional**. Solo apariciones de SPs en el listado `#478789` (todos codigo muerto).
    - 5 SPs identificados: `PR_ERP_FNZ_QRY_WS_CREAPROCESOFABRICACION` (ALTO muerto), `USP_PROD_PROCPROD_ELIMINAVALIDA` (MEDIO muerto), `USP_PROCESO_PRODUCCION`, `USP_PROCESO_PRODUCCION3`, `USP_PROCESO_CONFIGURACION1`.
    - Confirmado: los SPs NO existen en `mxbdaje_local` — eran de otras bases de datos del ecosistema Big Magic.
    - Documentacion AVAIL: MakeBySegments/MakeActs son de planificacion/ejecucion, no de configuracion de procesos.

2. **Busqueda de tablas de procesos en BD**: Se ejecutaron consultas con patrones `%proceso%`, `%propro%`, `%prgpro%`.
    - 8 tablas encontradas: `mproprod1f`, `mprocesos`, `ctm_proceso`, `ctm_proceso_area`, `ctm_proceso_linea`, `ctm_lista_proceso`, `mejecuta_procesos`, `psprgprod`.
    - 51 columnas en 35+ tablas con referencias a "proceso" — la mayoria en contexto de costos (CTM), no produccion.

3. **Hallazgo principal: `mproprod1f` vacia**: La tabla maestra de procesos productivos.
    - PK: `tipproprod` (codigo del tipo de proceso), campos: `descripcion`, `estado`, + auditoria.
    - **0 registros** en toda la tabla — ni Mexico ni ninguna otra compañia la poblo.
    - `mmateri7f.tipproprod` (FK) esta NULL en todos los registros — nunca se clasificaron materiales por proceso.

4. **Analisis de `ctm_proceso` (procesos globales)**: Tabla del modulo de costos con 6 macro-procesos.
    - 01 BEBIDAS, 02 COMPRESION, 03 INYECCION, 04 PLOTEO, 05 ALMACENES, 06 HIELO.
    - `ctm_proceso_area` mapea proceso→area (18 registros): BEBIDAS cubre 13 areas que coinciden con `mfameq1f.area` (Program #137).
    - `ctm_proceso_linea`: 132 registros para 17 compañias, pero **0 para Mexico (0030)**.
    - Conclusion: `ctm_proceso` es un catalogo de referencia util pero de granularidad macro, no de procesos individuales.

5. **Descarte de tablas auxiliares**:
    - `mprocesos` (0 registros): tabla generica de procesos batch/scheduler.
    - `ctm_lista_proceso` (14 registros): procesos de costeo (Standard Cost, Deviations), no produccion.
    - `mejecuta_procesos` (0 registros): scheduler de SPs.
    - `psprgprod` (0 registros): programacion de produccion.
    - **0 triggers, 0 routines** referenciando cualquiera de estas tablas.

### Tabla Resumen de Hallazgos Legacy

| Tabla | Registros | Proposito | Estado Real |
|---|---|---|---|
| `mproprod1f` | **0** | Maestro de tipos de proceso productivo | **Vacia** — tabla del Program #574, nunca operada |
| `mprocesos` | **0** | Procesos genericos (scheduler) | Vacia — no aplica |
| `ctm_proceso` | **6** | Macro-procesos industriales | **Datos de referencia** — BEBIDAS, COMPRESION, etc. |
| `ctm_proceso_area` | **18** | Mapeo proceso→area funcional | **Referencia** — areas coinciden con `mfameq1f` (#137) |
| `ctm_proceso_linea` | **132** | Proceso→linea por compañia | **0 para Mexico (0030)** — 17 otras compañias con datos |
| `ctm_lista_proceso` | **14** | Procesos de costeo CTM | No aplica — modulo de costos |
| `mejecuta_procesos` | **0** | Scheduler de procesos batch | Vacia — no aplica |
| `psprgprod` | **0** | Programacion de produccion | Vacia — modelo futuro |
| `mmateri7f.tipproprod` | NULL global | FK a `mproprod1f` | Nunca se clasificaron materiales por proceso |

### Decision de Arquitectura para Odoo 19

Al ser un "Clean Slate" (borron y cuenta nueva), se decidio **crear el modelo `bm.ctl.produccion.proceso` desde cero** con las siguientes decisiones:

1. **Modelo de procesos individuales (no macro)**: A diferencia de `ctm_proceso` que tiene 6 macro-categorias (BEBIDAS, COMPRESION...), este modelo define procesos productivos individuales (SOPLADO, LLENADO, ETIQUETADO, EMPACADO) que componen la cadena de fabricacion.

2. **Many2one a Categoria de Linea (#137) con `ondelete='restrict'`**: Protege la integridad referencial. Si una categoria de linea tiene procesos configurados, no se puede borrar. Usa el mismo patron que Program #138.

3. **Campo `secuencia` para orden de ejecucion**: Define el orden logico de los procesos en la cadena productiva (10=Soplado, 20=Jarabe, 30=Bases, 40=Llenado, 50=Etiquetado, 60=Empacado). Base para futuro calculo de tiempos estandar.

4. **Sin herencia de `mrp.workcenter`**: El modelo es independiente del modulo de Manufactura de Odoo. La conexion con Work Centers queda implicita via `categoria_linea_id` y puede agregarse en el futuro sin modificar este modelo.

5. **6 datos seed validados**: Los procesos iniciales se basan en la descripcion referencial (soplado, llenado, etiquetado, empacado) mas los mapeos de `ctm_proceso_area` que vinculan areas funcionales del Program #137.

6. **Compatibilidad con formato legacy**: Se mantienen los campos de auditoria en formato juliano (`feccrea` + 730000) y hora `HHMMSS` para consistencia con el resto de modulos.

### Implementacion del Agente

| Archivo | Estado |
|---|---|
| `models/program_574_proceso.py` | Nuevo — modelo `bm.ctl.produccion.proceso` |
| `views/program_574_proceso_views.xml` | Nuevo — list, form, search, action, menuitem |
| `data/program_574_proceso_data.xml` | Nuevo — 6 procesos seed (SOP, JAR, BAS, LLE, ETQ, EMP) |
| `models/__init__.py` | +linea 27 |
| `__manifest__.py` | +2 lineas (views + data) |
| `security/ir.model.access.csv` | +1 linea |
| `views/mantenimiento_configuracion.xml` | Sin cambios (placeholder intacto, menuitem se sobreescribe desde el nuevo XML) |

Datos seed cargados: 6 procesos con Many2one a `bm.ctl.produccion.categoria.linea` via `ondelete='restrict'`.

El menu `Mantenimiento → Configuraciones → Configura Procesos Productivos` ya apunta al nuevo modelo.

### Resumen Digerible: "La cadena de fabricacion que el legacy nunca configuro"

1. **Lo que hacia el sistema legacy**: Nada. La tabla `mproprod1f` existia estructuralmente pero jamas se poblo. Los Stored Procedures `USP_PROCESO_PRODUCCION` se crearon en 2013 como parte del diseño inicial pero nunca se desplegaron en Mexico. Los procesos productivos se manejaban implicitamente a traves de las recetas (BOMs) y la programacion de lineas, sin un catalogo explicito de "que procesos existen y en que orden se ejecutan".

2. **Lo que estamos haciendo en `models.py`**: Creamos un catalogo limpio de procesos productivos con codigo, descripcion, secuencia de ejecucion y vinculacion al area funcional via el Program #137. Cada proceso sabe a que categoria de linea pertenece (ej: SOPLADO → EQUIPOS DE SOPLADO, LLENADO → EQUIPOS DE ENVASADO). Los campos de auditoria mantienen el formato legacy para consistencia.

3. **Los 6 procesos cubren la cadena completa de bebidas**: En una planta de AJE, la fabricacion sigue un orden:
    - *SOP (Soplado, seq 10)*: Conversion de preformas PET en botellas. Area 026.
    - *JAR (Jarabe, seq 20)*: Mezclado de concentrados, azucar y agua en tanques. Area 025.
    - *BAS (Bases, seq 30)*: Preparacion de concentrados base. Area 032.
    - *LLE (Llenado, seq 40)*: Llenado de botellas con producto. Area 027.
    - *ETQ (Etiquetado, seq 50)*: Aplicacion de etiquetas. Area 031.
    - *EMP (Empacado, seq 60)*: Empaque en cajas y armado de tarimas. Area 051/053.

4. **La secuencia no es decorativa**: Define el orden real de la linea de produccion. Esto permitira en el futuro calcular tiempos estandar acumulados (ej: SOP(10) + LLE(40) = 50 unidades de tiempo total para una botella), validar que una OP no intente "etiquetar antes de llenar", y generar la hoja de ruta de fabricacion.

5. **Conexion con #137 y #138**: 
    - **#137** (Categorias): Define que areas funcionales existen (Envasado, Soplado, Etiquetas...). #574 asigna cada proceso al area correcta via Many2one.
    - **#138** (Familia): Configura que categorias operan en cada sucursal. #574 hereda esa restriccion implicitamente: si una sucursal no tiene activa la categoria "Envasado", no deberia poder asignar el proceso "Llenado" a lineas de esa sucursal.
    - **Flujo completo**: Categoria (#137) → Familia por sucursal (#138) → Proceso (#574) → Linea fisica (futuro).

### Detalle de los Scripts

#### `program_574_proceso.py` - El modelo principal

Este archivo define el modelo `bm.ctl.produccion.proceso` que cataloga los procesos productivos individuales.

**Estructura del modelo:**
- `_name = 'bm.ctl.produccion.proceso'`: Nombre tecnico en el ORM de Odoo.
- `_description`: "Proceso Productivo (Program 574)".
- `_order = 'secuencia, codigo'`: Ordenamiento por secuencia de ejecucion, luego codigo.

**Campos operativos:**
- `codigo` (Char, required): Codigo abreviado del proceso. 3 letras: SOP, JAR, BAS, LLE, ETQ, EMP.
- `descripcion` (Char, required): Nombre legible. Ej: "Soplado", "Preparacion de Jarabe", "Llenado / Envasado".
- `secuencia` (Integer, default=10): Orden en la cadena productiva. Multiplos de 10 para facilitar insercion de procesos intermedios.
- `categoria_linea_id` (Many2one → `bm.ctl.produccion.categoria.linea`, ondelete='restrict'): Area funcional asociada del Program #137. Bloquea borrado de categorias con procesos configurados.
- `activo` (Boolean, default=True): Switch de activacion.
- `company_id` (Many2one → `res.company`, default=lambda self: self.env.company): Compania propietaria.

**Campo computado:**
- `name` (Char, compute='_compute_name', store=True): Nombre generado como `{codigo} - {descripcion}`. Ej: "SOP - Soplado", "LLE - Llenado / Envasado". Depende de `codigo` y `descripcion`.

**Campos de auditoria (compatibilidad legacy):**
- `feccrea` (Integer, required): Fecha juliana. Calculo: `dias_desde_1_ene + 730000`.
- `horcrea` (Char, required): Hora `HHMMSS`.
- `usucrea` (Char, required): Login del usuario creador.
- `fecultmod`, `horultmod`, `usuaulmod`: Equivalentes para ultima modificacion.

**Metodos clave:**

1. `_default_fecha()` — Calcula el dia juliano para campos de auditoria. Mismo algoritmo que todos los modelos del modulo.

2. `_compute_name()` — Genera el nombre compuesto codigo + descripcion. Almacenado para busquedas.

3. `create()` (override con `@api.model_create_multi`) — Intercepta la creacion para poblar automaticamente `usucrea`, `feccrea`, `horcrea`. Respeta valores ya especificados.

4. `write()` (override) — Actualiza `usuaulmod`, `fecultmod`, `horultmod` en cada escritura.

#### `program_574_proceso_views.xml` - Las vistas

**List View (editable="bottom"):**
```xml
<list string="Procesos Productivos" editable="bottom">
    <field name="codigo"/>
    <field name="descripcion"/>
    <field name="secuencia"/>
    <field name="categoria_linea_id"/>
    <field name="activo"/>
</list>
```
- `editable="bottom"`: Creacion y edicion directa en lista. Ideal para catalogos maestros.
- 5 campos visibles: codigo, descripcion, secuencia, categoria y switch de activo.
- Orden: identificador → descripcion → secuencia → vinculo → estado.

**Form View:**
```xml
<form string="Proceso Productivo" edit="true">
    <sheet>
        <div class="oe_title">
            <h1><field name="name" readonly="1"/></h1>
        </div>
        <group>
            <group string="Configuracion">
                <field name="codigo"/>
                <field name="descripcion"/>
                <field name="secuencia"/>
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
- Titulo con nombre computado readonly.
- Dos grupos: Configuracion (editable) y Auditoria (solo lectura).

**Search View:**
```xml
<search string="Buscar Procesos Productivos">
    <field name="codigo"/>
    <field name="descripcion"/>
    <field name="categoria_linea_id"/>
    <separator/>
    <filter name="activos" string="Activos" domain="[('activo', '=', True)]"/>
    <filter name="inactivos" string="Inactivos" domain="[('activo', '=', False)]"/>
    <group>
        <filter name="grupo_categoria" string="Categoria" context="{'group_by': 'categoria_linea_id'}"/>
    </group>
</search>
```
- Busqueda por codigo, descripcion y categoria.
- Filtros rapidos Activos/Inactivos.
- Agrupacion por categoria de linea para analisis.

**Window Action:**
```xml
<record id="action_proceso" model="ir.actions.act_window">
    <field name="name">Procesos Productivos</field>
    <field name="res_model">bm.ctl.produccion.proceso</field>
    <field name="view_mode">list,form</field>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">
            Configura los procesos productivos
        </p>
        <p>
            Define los procesos que componen la fabricacion
            y su secuencia de ejecucion.
        </p>
    </field>
</record>
```

**Menu en Configuraciones:**
```xml
<menuitem id="menu_configura_procesos"
          name="Configura Procesos Productivos"
          parent="mant_configuraciones_menu"
          action="action_proceso"
          sequence="20"/>
```
- `sequence="20"`: Segundo item en Configuraciones, despues de Familia de Produccion (10).
- **Leccion de implementacion**: El menuitem se coloco en el mismo XML que define el action, no en `mantenimiento_configuracion.xml`, para evitar errores de orden de carga (el action debe existir antes que el menu lo referencie). El placeholder original en `mantenimiento_configuracion.xml` se mantiene intacto y es sobreescrito por este menuitem al cargarse despues.

#### `program_574_proceso_data.xml` - Datos iniciales

Archivo seed con `noupdate="1"` que carga 6 procesos productivos:

| XML ID | Codigo | Descripcion | Secuencia | Categoria (#137) |
|---|---|---|---|---|
| `proceso_soplado` | SOP | Soplado | 10 | 002 - EQUIPOS DE SOPLADO |
| `proceso_jarabe` | JAR | Preparacion de Jarabe | 20 | 003 - TANQUES DE JARABE |
| `proceso_bases` | BAS | Preparacion de Bases | 30 | 008 - BASES TERMINADAS |
| `proceso_llenado` | LLE | Llenado / Envasado | 40 | 001 - EQUIPOS DE ENVASADO |
| `proceso_etiquetado` | ETQ | Etiquetado | 50 | 025 - PRODUCCION ETIQUETAS |
| `proceso_empacado` | EMP | Empacado | 60 | 021 - REEMPAQUES |

**Notas sobre los datos seed:**
- `noupdate="1"`: El usuario puede modificar codigos, descripciones y secuencias sin que las actualizaciones del modulo los sobrescriban.
- Las referencias `categoria_001`, `categoria_002`, etc. usan nombres cortos (sin prefijo de modulo) — mismo patron que `program_138_familia_data.xml`.
- Secuencias en multiplos de 10 para permitir insercion de procesos intermedios (ej: un "Lavado de Botellas" podria insertarse como secuencia 15 entre Soplado y Jarabe).

#### `ir.model.access.csv` - Seguridad

```csv
access_bm_ctl_produccion_proceso,bm.ctl.produccion.proceso,model_bm_ctl_produccion_proceso,base.group_user,1,1,1,1
```
- Acceso total (CRUD) para `base.group_user`.

#### `__manifest__.py` - Orden de carga

```python
'views/mantenimiento_configuracion.xml',        # linea 24 — placeholder original (action dummy)
...
'data/program_138_familia_data.xml',            # linea 35
'views/program_574_proceso_views.xml',           # linea 36 — define action + menuitem (sobreescribe placeholder)
'data/program_574_proceso_data.xml',            # linea 37 — depende de categoria_X de linea 33
```
- El orden es critico: `program_137_categoria_linea_data.xml` (linea 33) debe cargarse antes que `program_574_proceso_data.xml` (linea 37) para que los External IDs `categoria_001`, etc. existan.
- `program_574_proceso_views.xml` se carga al final de las vistas para que su menuitem sobreescriba el placeholder de `mantenimiento_configuracion.xml`.

### Integracion Futura

1. **Hoja de Ruta de Fabricacion**: El campo `secuencia` permitira generar automaticamente la secuencia de operaciones para una orden de produccion, validando que los procesos se ejecuten en el orden correcto.

2. **Calculo de Tiempos Estandar**: Cada proceso podra tener un tiempo estandar asociado (futuro campo `tiempo_estandar`). La suma de tiempos por secuencia dara el tiempo total de fabricacion de un SKU.

3. **Conexion con Lineas Fisicas**: Cuando se implemente `bm.ctl.produccion.linea`, cada linea tendra un Many2one a proceso, indicando que proceso ejecuta esa linea. Esto permitira reportes de capacidad por proceso.

4. **Vinculo con Work Centers (`mrp.workcenter`)**: Si en el futuro se adopta el modulo de Manufactura de Odoo, cada `bm.ctl.produccion.proceso` podra mapearse a un `mrp.routing.workcenter` sin modificar este modelo — solo agregando un campo `workcenter_id`.

5. **Restriccion de secuencia**: Validacion a nivel de modelo que impida asignar la misma secuencia a dos procesos de la misma categoria, o que detecte huecos en la cadena (ej: falta un proceso entre secuencia 10 y 30).
