## validacion para program # 132  
El agente nos proporciona unas primeras descripciones para las funciones de BM-CTL-Produccion_Mexico.xlsx. Desde luego lee su bm_ctl_produccion_descripciones.md correspondiente, sin embargo; para validar realizamos consultas a la base de datos mxbdaje_local. Revisar [validacion program #: 132](data_para_agente/validaciones_programs/validacion_program_132.md)

### Logica de validacion y hallazgos Tecnicos
La validacion se realizó mediante un proceso de descarte y rastreo de datos en tres etapas, lo que permitió ajustar la estrategia de desarrollo para odoo 19:

1. **Investigacion de la infraestructura documental (Tablas de Turnos)**: Se ejecutaron consultas de volumetrias en las tablas **bturno1f**, **turno**, **turnoxop** y **relacionturno**.
   - **bturno1f**: 30 registros — maestra de definicion base de turnos (codigos 001, 002, 003) replicados por compañia.
   - **turno**: 55 registros — horarios reales por sucursal con hinicio/hfin en formato HHMMSS.
   - **turnoxop**: 37,155 registros — tabla transaccional masiva que vincula turnos con ordenes de produccion.
   - **relacionturno**: 14 registros — mapeo entre turnos de Big Magic y turnos del sistema AVAIL.
   - **Conclusion**: El sistema legacy maneja turnos de forma descentralizada. La maestra `bturno1f` solo define codigos, mientras que `turno` define horarios reales por sucursal. No hay una entidad unificada que combine definicion + horario.

2. **Rastreo de dispersión transversal**: Se auditaron 71 columnas en todo el esquema public que contienen referencias a "turno" o "shift".
   - **Hallazgo Critico**: La entidad "turno" esta dispersa en tablas de Logistica, Produccion, Auditoria e Inventarios. Predomina el tipo `text`, confirmando que el sistema usa **llaves naturales** (codigos como '001', '002') en lugar de IDs secuenciales.
   - **Interpretacion**: En Odoo 19, el modelo de turno debe ser referenciable desde todas estas estructuras transaccionales. La migracion requiere mapear codigos de texto a IDs de Odoo.

3. **Analisis de Integridad Cronologica y Triggers**: Se revisaron triggers y logica de negocio en las tablas de turnos.
   - **Resultado**: 0 triggers en las 4 tablas de turnos. Toda la logica de negocio esta en la capa de aplicacion del ERP legacy.
   - **Interpretacion**: La migracion a Odoo 19 es limpia — no hay efectos colaterales ocultos en la base de datos. Toda la logica se reimplementara en los modelos Python de Odoo.

### Decision de Arquitectura para Odoo 19
Basandose en estos hallazgos, se decidio evolucionar la estructura del sistema legacy:

1. **Unificacion de entidades**: En el legacy, la definicion de turnos (`bturno1f`) y los horarios por sucursal (`turno`) estan separados. En Odoo 19 se crearon 2 modelos relacionados:
   - `bm.ctl.produccion.turno.definicion` — catalogo global de turnos (hereda de `bturno1f`)
   - `bm.ctl.produccion.turno.horario` — horarios por sucursal (hereda de `turno`)
   Esto permite definir turnos base una vez y asignarlos a multiples sucursales con horarios especificos.

2. **Deteccion automatica de turnos nocturnos**: El legacy no tiene un campo explicito para turnos que cruzan medianoche. En Odoo 19 se agrego el campo computado `esnocturno` que detecta automaticamente cuando `horainicio > horafin` (ej: 220000 → 063000).

3. **Configuracion global centralizada**: Se creo `bm.ctl.produccion.config` para almacenar parametros globales como fecha inicial de migracion y turno por defecto, resolviendo la fragmentacion de configuracion del legacy.

4. **Fechas julianas con compatibilidad AS/400**: Se mantiene el formato juliano (base 730000) para compatibilidad con el sistema legacy, permitiendo que los datos de Odoo puedan ser leidos por el sistema anterior si es necesario.

### Implementacion del agente Qwen3.6 Plus
Se ha instruido al agente priorizar la logica de negocio en la capa de **models.py**. La base de datos legacy se utilizara unicamente como fuente de extraccion de codigos de turno y horarios para el mapeo inicial, pero la logica de gestion de turnos sera sustituida por un flujo de datos nativos de Odoo 19 que garantiza la integridad y consistencia ausente en el sistema original.

```bash
Implementation complete. Created Program#132 "Turnos de Produccion" with:
Models (3 files in models/):
- program_132_turno_definicion.py - Catalogo global de turnos (bturno1f)
- program_132_turno_horario.py - Horarios por sucursal (turno)
- program_132_produccion_config.py - Configuracion global (parametros)
Views (views/program_132_turnos.xml):
- Tree editable para turno_definicion
- Tree editable para turno_horario
- Tree editable para produccion_config
- Menu structure: Mantenimiento > Turnos > Catalogo, Horarios, Config
Security: security/ir.model.access.csv with full permissions
Updated: __manifest__.py, __init__.py
```

### Resumen Digerible: "dejar de usar hojas sueltas para pasarnos a un cuaderno organizado"

1. **Lo que hacia el sistema legacy**: Es como si tuvieras una lista de nombres de turnos (Turno 1, Turno 2, Turno 3) en una hoja, y en otra hoja diferente los horarios de cada sucursal. No hay una conexion clara entre ambas. Ademas, los horarios estan escritos como texto (ej: "220000") sin validacion de que sean horas reales.

2. **Lo que estamos haciendo en models.py**: Estamos creando un sistema donde primero defines los turnos base (como plantillas), y luego asignas esos turnos a cada sucursal con sus horarios especificos. Odoo validara automaticamente que los horarios sean correctos y detectara si un turno cruza medianoche.

3. **La base de datos vieja es solo un diccionario**: Solo vamos a entrar a la base de datos vieja para sacar los codigos de turno existentes (001, 002, 003) y los horarios por sucursal, para que cuando Odoo empiece a funcionar, ya tenga los datos basicos cargados.

4. **Odoo pone el orden**: A partir de ahora, Odoo obligara a que cada turno tenga un codigo unico, una descripcion clara y horarios validos. Ya no habra turnos duplicados o horarios inconsistentes como en el sistema legacy.

No se esta copiando el sistema viejo (que tiene inconsistencias), estamos usando el sistema viejo solo para saber que turnos existian y sus horarios, pero las nuevas reglas de validacion y orden las esta escribiendo el agente en el codigo de Odoo.

### Detalle de los scripts

#### program_132_turno_definicion.py — El catalogo base
Este es el modelo que reemplaza a `bturno1f`. Define los turnos globales que todas las sucursales pueden usar.

1. **Campo `codturno` (Integer, required)**: El codigo numerico del turno (1, 2, 3...). En el legacy era texto ('001'), aqui es integer para facilitar operaciones matematicas y ordenamiento.

2. **Campo `descripcion` (Char, required, default='Turno sin descripcion')**: Descripcion legible del turno. En el legacy existian dos campos (`descturno1` y `descturno2`) con variantes de formato. Aqui se unifica en uno solo.

3. **Campo `secuencia` (Integer, required, default=10)**: Define el orden de los turnos en listas y reportes. Multiplo de 10 para permitir inserciones intermedias sin renumerar.

4. **Campos `horainicio` y `horafin` (Char, default='060000' y '140000')**: Horarios estandar del turno en formato HHMMSS. Estos son horarios "base" que pueden ser sobrescritos por sucursal en el modelo `turno_horario`.

5. **Campo computado `esnocturno` (Boolean)**: Detecta automaticamente si el turno cruza medianoche comparando `horainicio > horafin`. Por ejemplo, un turno de 220000 a 063000 sera marcado como nocturno. Esto resuelve un problema del legacy donde no habia forma de identificar turnos nocturnos sin logica adicional.

6. **Campo computado `name` (Char, store=True)**: Genera un identificador legible como "T001 - Turno Dia". Se almacena en BD (`store=True`) para permitir busquedas y ordenamiento, pero se calcula automaticamente desde `codturno` y `descripcion`.

7. **Campos de auditoria**: `feccrea`, `horcrea`, `usucrea`, `fecultmod`, `horultmod`, `usuaulmod` — replican la estructura de auditoria del legacy con fechas julianas.

8. **Metodo `_default_fecha()`**: Convierte la fecha actual a formato juliano sumando 730000. Esto mantiene compatibilidad con el formato AS/400 del sistema legacy.

#### program_132_turno_horario.py — Horarios por sucursal
Este modelo reemplaza a `turno` y permite asignar turnos a sucursales especificas con horarios personalizados.

1. **Campo `sucursal` (Char, required)**: Codigo de la sucursal (ej: '0001', '0068'). En el legacy, la unicidad dependia de `(compania, sucursal, turno)`. Aqui se simplifica a sucursal + turno_id.

2. **Campo `turno_id` (Many2one, required)**: Relacion con `turno.definicion`. Esto es una mejora sobre el legacy donde la relacion era implicita por codigo de texto. Ahora hay una referencia explicita con integridad referencial.

3. **Campos relacionados `codturno`, `horainicio`, `horafin`, `esnocturno`**: Se traen automaticamente del turno padre mediante `related`. Esto permite ver la informacion del turno base sin duplicar datos.

4. **Campo computado `name` (Char, store=True)**: Genera un identificador como "0001 - T001 - Turno Dia" combinando sucursal y turno. Facilita la identificacion visual en listas.

5. **Sobrecarga de `create()` y `write()`**: Actualiza automaticamente los campos de auditoria (`usucrea`, `feccrea`, `horcrea`, etc.) si no se proporcionan explicitamente. Esto garantiza que siempre haya trazabilidad de quien creo o modifico cada registro.

#### program_132_produccion_config.py — Configuracion global
Este modelo no tiene equivalente directo en el legacy. Centraliza parametros globales de produccion que estaban dispersos en multiples tablas.

1. **Campo `compania` (Char, required, default='0030')**: Compañia configurada. En el legacy, cada tabla tenia su propio campo `compania`. Aqui se centraliza.

2. **Campo `fecha_inicial_prod` (Integer, juliano)**: Fecha desde la cual se migran/muestran datos de produccion. Permite filtrar datos historicos durante la migracion.

3. **Campo computado `fecha_inicial_prod_display` (Date)**: Convierte la fecha juliana a formato Date legible para la UI. La conversion usa la formula: `base = date(year, 1, 1) + timedelta(days=fecha_juliana - 730000 - 1)`.

4. **Campo `turno_default_id` (Many2one)**: Turno por defecto para nuevas operaciones. En el legacy, este parametro estaba implicito o disperso en tablas de configuracion.

5. **Campos de auditoria**: Misma estructura que los otros modelos, garantizando consistencia en la trazabilidad.

#### views/program_132_turnos.xml — La interfaz
Define las vistas y menus para los 3 modelos del programa 132.

1. **Vista lista de `turno_definicion` (editable="bottom")**: Permite crear y editar turnos directamente en la lista. Campos visibles: secuencia, codturno, descripcion, horainicio, horafin, esnocturno.

2. **Vista form de `turno_definicion`**: Formulario completo con grupos:
   - "Informacion del Turno": codturno, descripcion, secuencia
   - "Horario": horainicio, horafin, esnocturno
   - "Auditoria": campos de auditoria readonly

3. **Vista lista de `turno_horario` (editable="bottom")**: Permite asignar turnos a sucursales directamente en la lista. Campos visibles: sucursal, turno_id, codturno, horainicio, horafin, esnocturno.

4. **Vista lista de `produccion_config` (editable="bottom")**: Configuracion rapida de parametros globales. Campos visibles: compania, fecha_inicial_prod, fecha_inicial_prod_display, turno_default_id.

5. **Estructura de menus**:
   ```
   Mantenimiento > Turnos (carpeta)
     ├── Catalogo de Turnos (secuencia 10)
     ├── Horarios por Sucursal (secuencia 20)
     ── Configuracion Global (secuencia 30)
   ```
   El menu padre "Turnos" no tiene accion, solo actua como contenedor. Esto evita el problema de Odoo donde un menu con hijos no muestra su accion propia.

6. **Secuencias multiplos de 10**: Todas las secuencias de menus siguen el estandar del proyecto (10, 20, 30) para permitir inserciones futuras sin renumerar.

#### security/ir.model.access.csv — Permisos
Define permisos de acceso para los 3 modelos:
- `bm.ctl.produccion.turno.definicion` — acceso total para `base.group_user`
- `bm.ctl.produccion.turno.horario` — acceso total para `base.group_user`
- `bm.ctl.produccion.config` — acceso total para `base.group_user`

Esto permite que cualquier usuario autenticado pueda gestionar turnos sin restricciones adicionales.

#### __init__.py — Orden de carga
El orden de importacion es critico para evitar errores de dependencias:
1. `program_132_turno_definicion` — modelo base, no depende de nadie
2. `program_132_turno_horario` — depende de `turno_definicion` (Many2one)
3. `program_132_produccion_config` — depende de `turno_definicion` (Many2one)

Si se intentara cargar `turno_horario` antes que `turno_definicion`, Odoo lanzaria un error diciendo que el modelo de destino no existe todavia.

### Mapeo Legacy → Odoo 19

| Tabla Legacy | Modelo Odoo | Relacion |
|---|---|---|
| `bturno1f` | `bm.ctl.produccion.turno.definicion` | 1:1 (maestra de turnos) |
| `turno` | `bm.ctl.produccion.turno.horario` | 1:1 (horarios por sucursal) |
| `turnoxop` | Sin modelo directo | Tabla transaccional, se migrara como datos historicos |
| `relacionturno` | Sin modelo directo | Mapeo BM-AVAIL, no aplica en Odoo |
| `horpro`, `opxlinea`, `proptur`, `dproptur` | Sin modelo directo | Tablas consumidoras del dato "turno", se referenciaran via Many2one |

### Volumetria de datos a migrar

| Tabla | Registros | Tipo | Estrategia de migracion |
|---|---|---|---|
| `bturno1f` | 30 | Maestra | Migracion completa |
| `turno` | 55 | Maestra | Migracion completa |
| `turnoxop` | 37,155 | Transaccional | Solo periodo activo (ultimo año) |
| `relacionturno` | 14 | Configuracion | No aplica en Odoo |

Total aproximado: ~85 registros maestros + datos transaccionales filtrados.
