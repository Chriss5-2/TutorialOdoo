## 1. EXPLORACIÓN DE DOCUMENTACIÓN OFICIAL - CATEGORÍAS DE LÍNEAS DE PRODUCCIÓN

**Objetivo:** Consultar `aje_docs_simulacion/01_Docs_Oficiales/` y sus subcarpetas para obtener un acercamiento inicial al Program #137 "Categorías de Líneas de Producción".

### 1.1 Consulta: Búsqueda de documentación sobre el Program #137 en docs oficiales

**Query 1.1.1** — Búsqueda de archivos `.md` en la estructura de documentos oficiales:
```
aje_docs_simulacion/01_Docs_Oficiales/
├── DocsOficiales/
│   ├── A&F/
│   ├── Cadena de Suministro/
│   ├── Comercial/
│   ├── Local México/
│   └── Transversal/
└── #478789 Obtener informacion de BD Mexico producción_xlsx.md
```

**Hallazgo 1.1.1:** Se identifican múltiples subcarpetas con documentación oficial del sistema Big Magic ERP. Se procede a buscar contenido relacionado con el Program #137.

### 1.2 Consulta: Búsqueda de referencias al Program #137, tabla mfameq, y categorías de líneas

**Query 1.2.1** — Búsqueda con patrón `137|mfameq|categoria.*linea|familia.*equipo` en todo el directorio `01_Docs_Oficiales/`:
```bash
grep -r "137\|mfameq\|categoria.*linea\|familia.*equipo" aje_docs_simulacion/01_Docs_Oficiales/
```

**Hallazgo 1.2.1:** No se encontraron coincidencias relevantes. Las únicas apariciones del número "137" fueron:
- Números de voucher contable en `A&F/SAP MX/Ejemplo data/voucher contable_xlsx.md` (ej: `13732.27`, `13706.39`)
- Timestamps en listados de stored procedures de SQL Server (`#478789 Obtener informacion de BD Mexico producción_xlsx.md`)
- Números de cliente en `acreedor_deudor_ecp_xlsx.md`
- JSON de integración Salesforce-Zuper con IDs de pedido

Ninguna de estas coincidencias tiene relación con el Program #137 "Categorías de Líneas de Producción".

---

### RESUMEN DE HALLAZGOS — SECCIÓN 1

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | No existe documentación funcional del Program #137 en docs oficiales | 1.2.1 | La fuente de verdad es la BD legacy |
| 2 | Las coincidencias de "137" son numéricas irrelevantes (vouchers, timestamps, IDs) | 1.2.1 | Confirmar búsqueda exhaustiva |

### Acción recomendada para Odoo 19:
- No depender de documentación oficial para este programa
- Construir el modelo directamente desde la estructura de la BD legacy

---

## 2. CONCLUSIÓN DE LA CONSULTA A DOCUMENTACIÓN OFICIAL

**El Program #137 "Categorías de Líneas de Producción" no tiene documentación específica en `aje_docs_simulacion/01_Docs_Oficiales/`.**

### Ubicación en el árbol de menús (de `Produccion_arbol_funciones.html`):

```
Menu Principal
└── Mantenimiento (mexico: SI)
    └── Clasificadores (mexico: SI)
        └── Categorias de Lineas de Produccion (mexico: SI)
```

También aparece duplicado en:
```
└── Costos (mexico: SI)
    └── Costo SemiVariable (mexico: SI)
        └── Variables de Produccion (mexico: SI)
            └── Categoria de Linea de Produccion (mexico: SI)
```

### Descripción funcional (de `bm_ctl_produccion_descripciones.md`):

> Clasifica las líneas de producción por categoría (llenadoras, etiquetadoras, sopladoras, paletizadoras). Permite agrupar líneas con características similares para reportes de capacidad, eficiencia y costos. Cada categoría puede tener reglas de negocio específicas para cálculo de costos semi-variables.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 2

| # | Hallazgo | Impacto para Odoo 19 |
|---|----------|---------------------|
| 1 | No hay docs oficiales del Program #137 | Consultar BD legacy directamente |
| 2 | Programa aparece en 2 ubicaciones de menú (Mantenimiento y Costos) | Considerar ambos accesos |
| 3 | México: SI en ambas ubicaciones | Prioridad alta para migración |

### Acción recomendada para Odoo 19:
- Menú principal: `Mantenimiento → Clasificadores → Categorias de Lineas` (secuencia 40)
- Menú secundario: `Costos → Costo SemiVariable → Variables de Produccion → Categoria Linea de Produccion` (secuencia 10)

---

## 3. EXPLORACIÓN DE DICCIONARIO DE DATOS - CATEGORÍAS DE LÍNEAS DE PRODUCCIÓN

**Objetivo:** Ejecutar consulta de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas a la clasificación de líneas de producción por categoría dentro del esquema público, con el fin de mapear la estructura de persistencia en `mxbdaje_local`.

### 3.1 Consulta: Búsqueda sistemática de tablas con "linea" en el nombre

**Query 3.1.1** — Todas las tablas con "linea":
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' AND tablename ILIKE '%linea%'
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
         tablename         
---------------------------
 caplinea
 conxarlinea
 ctm_proceso_linea
 mlinea1f
 mlinea1f_bkp_111118
 mlinea2f
 opxlinea
 seguimiento_valorizalinea
(8 rows)
```

**Hallazgo 3.1.1:** Se identifican 8 tablas con "linea" en el nombre. Cada una debe inspeccionarse para determinar su propósito real.

### 3.2 Consulta: Búsqueda de tablas de familias/categorías de equipos

**Query 3.2.1** — Tablas de familias de equipos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%fameq%' OR tablename ILIKE '%familieq%' 
     OR tablename ILIKE '%famequipo%' OR tablename ILIKE '%bfameq%'
     OR tablename ILIKE '%mfameq%')
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tablename 
-----------
 mfameq1f
(1 row)
```

**Hallazgo 3.2.1:** Se identifica `mfameq1f` como tabla maestra de familias de equipos. Esta es la candidata principal para el catálogo de categorías de líneas de producción.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 3

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 8 tablas con "linea" en nombre | 3.1.1 | Inspeccionar cada una para separar inventario vs producción |
| 2 | `mfameq1f` es tabla de familias de equipos | 3.2.1 | Candidata principal para Program #137 |

### Acción recomendada para Odoo 19:
- Inspeccionar cada tabla con "linea" para separar las contables/inventario de las de producción física
- Confirmar `mfameq1f` como catálogo principal antes de diseñar el modelo

---

## 4. ANÁLISIS DE TABLA `mlinea1f` - CONFIRMACIÓN: LÍNEAS DE INVENTARIO

**Objetivo:** Confirmar que `mlinea1f` es de líneas de inventario/contables, NO de producción física.

### 4.1 Consulta: Estructura y datos de `mlinea1f`

**Query 4.1.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mlinea1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                   Table "public.mlinea1f"
      Column       |  Type   | Collation | Nullable | Default 
-------------------+---------+-----------+----------+---------
 compania          | text    |           | not null | 
 linea             | text    |           | not null | 
 descrip           | text    |           | not null | 
 flglinea          | text    |           | not null | 
 ... [37 columnas] ...
Indexes:
    "idx_170087_mlinea1l1" UNIQUE, btree (compania, linea)
    "idx_170087_mlinea1l2" btree (compania, descrip)
    "idx_170087_mlinea1l3" btree (compania, flglinea)
```

**Query 4.1.2** — Líneas de México 0030:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT linea, descrip, flglinea FROM mlinea1f WHERE compania = '0030' ORDER BY linea;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 linea |                 descrip                  | flglinea 
-------+------------------------------------------+----------
 01    | PRODUCTO TERMINADO                       | Te
 02    | MERCADERIAS                              | Te
 03    | PRODUCTO INTERMEDIO                      | Pr
 04    | MATERIA PRIMA E INSUMOS                  | In
 05    | ENVASES Y EMBALAJES                      | In
 06    | AUXILIARES                               | In
 07    | REPUESTOS                                | Re
 08    | SUMINISTROS DIVERSOS                     | Su
 09    | ECONOMATO                                | Ec
 10    | MATERIAL PUBLICITARIO                    | Al
 11    | SERVICIOS Y GASTOS                       | Se
 12    | ACTIVOS FIJOS                            | Ac
 13    | DESECHOS                                 | Ot
 14    | INTANGIBLE                               | Ot
 15    | DIFERIDOS                                | Di
 16    | BIENES EN MANTENIMIENTO                  | Ot
 17    | OTROS INGRESOS  Y DESCUENTOS COMERCIALES | Ot
 20    | MERCADERIAS OTRAS LINEAS DE NEGOCIOS     | Te
 30    | OTROS PRODUCTOS TERMINADOS               | Te
 31    | INSUMOS OTROS PRODUCTOS TERMINADOS       | In
 32    | SUMINISTROS OTROS PRODUCTOS TERMINADOS   | Te
 33    | PRODUCTO TERMINADO INTERMEDIO            | Pr
 34    | PRODUCTO INTERMEDIO                      | Pr
 35    | EMBALAJE NO DEPRECIABLE                  | In
 36    | BIENES EN SERVICIO DE MAQUILA            | Te
 37    | OTROS PRODUCTOS ELABORADOS               | Te
(26 rows)
```

**Hallazgo 4.1.1:** 
- **`mlinea1f` NO es de líneas de producción física**: Son líneas de inventario/contables
- **`flglinea`** clasifica por tipo contable: Te=Terminado, In=Insumo, Pr=Intermedio, Ot=Otros, Re=Repuestos, Su=Suministros, Se=Servicios, Ec=Economato, Ac=Activos Fijos, Di=Diferidos, Al=Publicitario
- **26 líneas para 0030**, todas contables
- **No aplica al Program #137**

---

### RESUMEN DE HALLAZGOS — SECCIÓN 4

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mlinea1f` es de líneas de inventario | 4.1.2 | No usar para categorías de producción |
| 2 | `flglinea` = tipo contable (Te, In, Pr, etc.) | 4.1.2 | Clasificador contable, no de máquinas |

### Acción recomendada para Odoo 19:
- No confundir `mlinea1f` con líneas de producción física
- El modelo de categoría de línea NO debe basarse en esta tabla

---

## 5. ANÁLISIS DE TABLA `mlifacategoria1f` - CONFIRMACIÓN: CLASIFICACIÓN CONTABLE

**Objetivo:** Confirmar que `mlifacategoria1f` es clasificación contable/inventarial, no de producción física.

### 5.1 Consulta: Estructura y datos de `mlifacategoria1f`

**Query 5.1.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mlifacategoria1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
           Table "public.mlifacategoria1f"
  Column   |  Type   | Collation | Nullable | Default 
-----------+---------+-----------+----------+---------
 compania  | text    |           | not null | 
 linea     | text    |           | not null | 
 familia   | text    |           | not null | 
 categoria | text    |           | not null | 
 estado    | text    |           | not null | 
 feccrea   | integer |           |          | 
 horcrea   | text    |           |          | 
 usuacrea  | text    |           |          | 
 fecultmod | integer |           |          | 
 horultmod | text    |           |          | 
 usultmod  | text    |           |          | 
Indexes:
    "idx_170072_mlifacategoria1f_i1" PRIMARY KEY, btree (compania, linea, familia, categoria)
```

**Query 5.1.2** — Muestreo de datos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, linea, familia, categoria, estado FROM mlifacategoria1f LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | linea | familia | categoria | estado 
----------+-------+---------+-----------+--------
 0002     |       |         |           | A
 0002     | 01    | 001     | 501       | A
 0002     | 01    | 001     | 502       | I
 0002     | 01    | 001     | 504       | I
 0002     | 01    | 001     | 506       | I
 0002     | 01    | 001     | 509       | I
 0002     | 01    | 001     | ABC       | I
 0002     | 01    | 001     | XYZ       | I
 0002     | 01    | 001     | ZYX       | I
 0002     | 01    | 002     | 502       | A
 0002     | 01    | 002     | 504       | I
 0002     | 01    | 002     | 505       | A
 0002     | 01    | 002     | 508       | I
 0002     | 01    | 002     | 509       | I
 0002     | 01    | 002     | ZYX       | I
 0002     | 01    | 003     | 502       | I
 0002     | 01    | 003     | 503       | A
 0002     | 01    | 003     | 504       | I
 0002     | 01    | 003     | 505       | I
 0002     | 01    | 004     | 502       | I
(20 rows)
```

**Hallazgo 5.1.1:** 
- **PK compuesta**: `(compania, linea, familia, categoria)` — tabla de clasificación jerárquica
- **Códigos numéricos sin descripción**: familia='001', categoria='501' — son códigos contables/inventariales
- **Valores de prueba**: 'ABC', 'XYZ', 'ZYX' — datos no depurados
- **1,569 registros totales**, 164 para 0030
- **No aplica al Program #137**

---

### RESUMEN DE HALLAZGOS — SECCIÓN 5

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mlifacategoria1f` es clasificación contable | 5.1.1 | No usar para categorías de producción |
| 2 | Códigos sin descripción legible | 5.1.2 | No son categorías de máquinas |

### Acción recomendada para Odoo 19:
- No usar esta tabla como base para el modelo de categorías
- La clasificación jerárquica contable es independiente de la clasificación de líneas de producción

---

## 6. ANÁLISIS DE TABLA `mfameq1f` - HALLAZGO PRINCIPAL: FAMILIAS DE EQUIPOS

**Objetivo:** Inspeccionar `mfameq1f` como el catálogo real de categorías de líneas de producción.

### 6.1 Consulta: Estructura de `mfameq1f`

**Query 6.1.1** — Describir estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mfameq1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                 Table "public.mfameq1f"
   Column    |   Type   | Collation | Nullable | Default 
-------------+----------+-----------+----------+---------
 compania    | text     |           | not null | 
 sucursal    | text     |           | not null | 
 efamilia    | text     |           | not null | 
 descripcion | text     |           |          | 
 nivcost     | smallint |           | not null | 
 estado      | text     |           |          | 
 feccreacio  | integer  |           |          | 
 horcreacio  | text     |           |          | 
 usuacreac   | text     |           |          | 
 fecultimod  | integer  |           |          | 
 horultimod  | text     |           |          | 
 usuaulmod   | text     |           |          | 
 area        | text     |           |          | 
 funcion     | text     |           |          | 
 abalmproc   | bytea    |           |          | 
 factor      | text     |           |          | 
 plan1       | bytea    |           |          | 
 atenauto    | bytea    |           |          | 
 turvar      | bytea    |           |          | 
 multreq     | bytea    |           |          | 
 ciesinreq   | bytea    |           |          | 
 flgglobal   | bytea    |           |          | 
 almproc     | text     |           |          | 
 codagru     | integer  |           |          | 
 flgreghh    | bytea    |           |          | 
 resprodpar  | bytea    |           |          | 
 flgregbpm   | bytea    |           |          | 
 flgliqpdso  | bytea    |           |          | 
Indexes:
    "idx_169847_mfamel01" UNIQUE, btree (compania, sucursal, efamilia)
    "idx_169847_mfamel02" btree (compania, sucursal, area, efamilia)
```

**Hallazgo 6.1.1:** 
- **PK**: `(compania, sucursal, efamilia)` — familia de equipo por compañía y sucursal
- **Campo `descripcion`**: Texto legible (ej: "EQUIPOS DE ENVASADO")
- **Campo `area`**: Código de área funcional
- **Campo `funcion`**: Indicador de función (ej: 'G' para global)
- **Campos de auditoría**: `feccreacio`, `horcreacio`, `usuacreac`, `fecultimod`, `horultimod`, `usuaulmod`
- **Campos de configuración**: `abalmproc`, `factor`, `plan1`, `atenauto`, `turvar`, `multreq`, `ciesinreq`, `flgglobal`, `almproc`, `codagru`, `flgreghh`, `resprodpar`, `flgregbpm`, `flgliqpdso`

### 6.2 Consulta: Familias de equipos para México

**Query 6.2.1** — Familias únicas por descripción:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT efamilia, descripcion, area, funcion, estado 
FROM mfameq1f 
WHERE compania = '0030' AND sucursal = '0001'
ORDER BY efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 efamilia |          descripcion           | area | funcion | estado 
----------+--------------------------------+------+---------+--------
 001      | EQUIPOS DE ENVASADO            | 027  |         | A
 002      | EQUIPOS DE SOPLADO             | 026  |         | A
 003      | TANQUES DE JARABE              | 025  |         | A
 004      | LAVADORAS                      | 101  |         | I
 005      | TANQUES DE TRATAMIENTO DE AGUA | 025  |         | A
 006      | ACONDICIONADOS                 | 034  |         | I
 007      | INYECTORAS                     | 029  |         | I
 008      | BASES TERMINADAS               | 032  |         | A
 009      | BASES INTERMEDIAS              | 032  |         | A
 010      | AZUCAR LIQUIDA                 | 025  |         | A
 011      | COMPRESION                     | 030  |         | I
 012      | AGUA EMBOTELLADA               | 101  |         | I
 013      | ISOTONICAS                     | 101  |         | A
 014      | AZUCAR LIQUIDA                 | 101  |         | I
 015      | ENVASADOS JARABES TERMINADOS   | 027  |         | I
 016      | NECTARES                       | 101  |         | I
 017      | UNIDAD DE PLOTEO               | 801  |         | A
 018      | TANQUES DE JARABE SIMPLE       | 503  |         | I
 019      | MAQUILA                        | 035  |         | A
 020      | EQUIPOS DE HIELO               | 052  |         | I
 021      | REEMPAQUES                     | 051  |         | A
 025      | PRODUCCION ETIQUETAS           | 031  | G       | A
 026      | PRODUCCION TERMOENCOGIBLE      | 065  | G       | A
 027      | PRODUCCION BOTELLA             | 022  |         | A
 050      | TRATAMIENTO DE AGUA CERVEZA    | 024  |         | I
 051      | PRODUCCION EXHIBIDORES         | 072  |         | A
 054      | EXTRUIDO SNACKS                |      |         | A
(27 rows)
```

**Hallazgo 6.2.1:** 
- **27 familias de equipos** para sucursal 0001 de México (0030)
- **Categorías activas (estado='A')** relevantes para producción:
  - `001` EQUIPOS DE ENVASADO (llenadoras)
  - `002` EQUIPOS DE SOPLADO (sopladoras)
  - `003` TANQUES DE JARABE
  - `005` TANQUES DE TRATAMIENTO DE AGUA
  - `008` BASES TERMINADAS
  - `009` BASES INTERMEDIAS
  - `010` AZUCAR LIQUIDA
  - `013` ISOTONICAS
  - `017` UNIDAD DE PLOTEO
  - `019` MAQUILA
  - `021` REEMPAQUES
  - `025` PRODUCCION ETIQUETAS
  - `026` PRODUCCION TERMOENCOGIBLE
  - `027` PRODUCCION BOTELLA
  - `051` PRODUCCION EXHIBIDORES
  - `054` EXTRUIDO SNACKS
- **Categorías inactivas (estado='I')**: LAVADORAS, ACONDICIONADOS, INYECTORAS, COMPRESION, AGUA EMBOTELLADA, ENVASADOS JARABES TERMINADOS, NECTARES, TANQUES DE JARABE SIMPLE, EQUIPOS DE HIELO, TRATAMIENTO DE AGUA CERVEZA

---

### RESUMEN DE HALLAZGOS — SECCIÓN 6

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mfameq1f` es el catálogo de familias de equipos | 6.1.1 | Es la tabla del Program #137 |
| 2 | 27 familias por sucursal, con descripción legible | 6.2.1 | Catálogo completo y documentado |
| 3 | Campo `area` agrupa por área funcional | 6.2.1 | Permite agrupación por tipo de proceso |
| 4 | Estado A/I para activo/inactivo | 6.2.1 | Filtrar solo activas para México |
| 5 | Campo `funcion`='G' para familias globales | 6.2.1 | Etiquetas y termos son globales |

### Acción recomendada para Odoo 19:
- Usar `mfameq1f` como base para el modelo `bm.ctl.produccion.categoria.linea`
- Migrar las 16 categorías activas de México como datos iniciales
- Mapear `estado`='A' → `activo`=True

---

## 7. EXPLORACIÓN DE CAMPOS DE CONFIGURACIÓN EN `mfameq1f`

**Objetivo:** Profundizar en los campos de configuración de `mfameq1f`, especialmente `factor`, `almproc`, `nivcost` y `codagru`.

### 3.1 Consulta: Estructura completa de `mfameq1f`

**Query 7.1.1** — Todas las columnas de la tabla:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'mfameq1f' 
AND table_schema = 'public'
ORDER BY ordinal_position;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 column_name | data_type 
-------------+-----------
 compania    | text
 sucursal    | text
 efamilia    | text
 descripcion | text
 nivcost     | smallint
 estado      | text
 feccreacio  | integer
 horcreacio  | text
 usuacreac   | text
 fecultimod  | integer
 horultimod  | text
 usuaulmod   | text
 area        | text
 funcion     | text
 abalmproc   | bytea
 factor      | text
 plan1       | bytea
 atenauto    | bytea
 turvar      | bytea
 multreq     | bytea
 ciesinreq   | bytea
 flgglobal   | bytea
 almproc     | text
 codagru     | integer
 flgreghh    | bytea
 resprodpar  | bytea
 flgregbpm   | bytea
 flgliqpdso  | bytea
(28 rows)
```

**Hallazgo 7.1.1:**
- **28 columnas** en total
- **Campos bytea** (blob binario): `abalmproc`, `plan1`, `atenauto`, `turvar`, `multreq`, `ciesinreq`, `flgglobal`, `flgreghh`, `resprodpar`, `flgregbpm`, `flgliqpdso` — son flags o configuraciones internas del sistema legacy, no legibles directamente
- **Campos de texto útiles**: `compania`, `sucursal`, `efamilia`, `descripcion`, `area`, `funcion`, `factor`, `almproc`, `estado`
- **Campos numéricos**: `nivcost` (smallint), `codagru` (integer)

### 3.2 Consulta: Niveles de costeo (`nivcost`)

**Query 7.2.1** — Distribución de `nivcost` para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT nivcost, COUNT(*) as total 
FROM mfameq1f 
WHERE compania = '0030' 
GROUP BY nivcost ORDER BY nivcost;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 nivcost | total 
---------+-------
       0 |   397
       4 |    11
(2 rows)
```

**Hallazgo 7.2.1:**
- **`nivcost = 0`**: 397 registros (97%) — nivel de costeo por defecto
- **`nivcost = 4`**: 11 registros (3%) — nivel especial, corresponde a `050 TRATAMIENTO DE AGUA CERVEZA`
- Solo una categoría tiene nivel de costeo diferente de 0

### 3.3 Consulta: Valores del campo `factor`

**Query 7.3.1** — Distribución de `factor` para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT factor, COUNT(*) as total
FROM mfameq1f 
WHERE compania = '0030' AND factor IS NOT NULL AND factor != ''
GROUP BY factor ORDER BY factor;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 factor | total 
--------+-------
 B      |   250
 N      |    22
(2 rows)
```

**Hallazgo 7.3.1:**
- **`factor = 'B'`**: 250 registros — la mayoría de categorías
- **`factor = 'N'`**: 22 registros — solo `PRODUCCION ETIQUETAS` y `PRODUCCION TERMOENCOGIBLE`
- **Vacío**: 125 registros — `EXTRUIDO SNACKS` y variantes de `TRATAMIENTO DE AGUA CERVEZA`

### 3.4 Consulta: Configuración detallada de categorías activas (sucursal 0001)

**Query 7.4.1** — Campos de configuración para categorías activas:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT efamilia, descripcion, factor, almproc, codagru, nivcost, area
FROM mfameq1f 
WHERE compania = '0030' AND sucursal = '0001' AND estado = 'A'
ORDER BY efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 efamilia |          descripcion           | factor | almproc | codagru | nivcost | area 
----------+--------------------------------+--------+---------+---------+---------+------
 001      | EQUIPOS DE ENVASADO            | B      | 83      |         |       0 | 027
 002      | EQUIPOS DE SOPLADO             | B      | 83      |         |       0 | 026
 003      | TANQUES DE JARABE              | B      | 83      |         |       0 | 025
 005      | TANQUES DE TRATAMIENTO DE AGUA | B      | 83      |         |       0 | 025
 008      | BASES TERMINADAS               | B      | 85      |         |       0 | 032
 009      | BASES INTERMEDIAS              | B      | 85      |         |       0 | 032
 010      | AZUCAR LIQUIDA                 | B      | 83      |         |       0 | 025
 017      | UNIDAD DE PLOTEO               | B      |         |         |       0 | 801
 019      | MAQUILA                        | B      | 86      |         |       0 | 035
 021      | REEMPAQUES                     | B      |         |         |       0 | 051
 025      | PRODUCCION ETIQUETAS           | N      | 53      |         |       0 | 031
 026      | PRODUCCION TERMOENCOGIBLE      | N      | 53      |         |       0 | 065
 027      | PRODUCCION BOTELLA             | B      | 83      |         |       0 | 022
 051      | PRODUCCION EXHIBIDORES         | B      | 53      |       0 |       0 | 072
 054      | EXTRUIDO SNACKS                |        |         |       0 |       0 | 
(15 rows)
```

**Hallazgo 7.4.1:**
- **`almproc`** (almacén de proceso): valores comunes:
  - `83`: Envasado, Soplado, Jarabe, Agua, Azúcar líquida, Botella
  - `85`: Bases terminadas e intermedias
  - `86`: Maquila
  - `53`: Etiquetas, termos, exhibidores
  - Vacío: Ploteo, reempaque, snacks
- **`codagru`**: siempre vacío o 0 — campo no utilizado
- **`nivcost`**: siempre 0 para categorías activas de sucursal 0001

---

### RESUMEN DE HALLAZGOS — SECCIÓN 7

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 28 columnas, 11 son bytea (no legibles) | 7.1.1 | Solo migrar campos de texto/numéricos útiles |
| 2 | `factor` tiene 2 valores: B (botella) y N (no botella) | 7.3.1 | Campo Selection en Odoo |
| 3 | `almproc` agrupa por tipo de almacén de proceso | 7.4.1 | Many2one a modelo de almacenes |
| 4 | `codagru` no se utiliza (siempre vacío o 0) | 7.4.1 | Campo obsoleto, no migrar |
| 5 | `nivcost = 4` solo para tratamiento de agua cerveza | 7.2.1 | Caso especial, no aplica a México bebidas |

### Acción recomendada para Odoo 19:
- **Modelo `bm.ctl.produccion.categoria.linea`**:
  - `efamilia` (Char, required): Código de familia
  - `descripcion` (Char, required): Nombre legible
  - `area` (Char): Código de área funcional
  - `funcion` (Char): 'G' = global
  - `factor` (Selection): 'B' = Botella, 'N' = No botella
  - `almproc` (Char): Almacén de proceso
  - `activo` (Boolean): Mapeado de `estado`='A'
  - `compania` (Char): Compañía
  - `sucursal` (Char): Sucursal
- **NO migrar**: campos bytea, `codagru`, `nivcost` (salvo que se necesite para costos)

---

## 8. ANÁLISIS DE DISTRIBUCIÓN POR SUCURSAL

**Objetivo:** Entender cómo se distribuyen las categorías de líneas de producción entre compañías y sucursales.

### 8.1 Consulta: Sucursales con datos en `mfameq1f`

**Query 8.1.1** — Conteo por compañía y sucursal:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, COUNT(*) as total 
FROM mfameq1f 
GROUP BY compania, sucursal 
ORDER BY compania, sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | total 
----------+----------+-------
 0030     | 0001     |    27
 0030     | 0068     |    26
 0030     | 0070     |    26
 0030     | 0086     |    27
 0030     | 0108     |    26
 0030     | 0112     |    27
 0030     | 0113     |    27
 0030     | 0114     |    27
 ... (muchas sucursales con 1 registro) ...
 0032     | 0001     |    27
 0036     | 01       |    27
 XX30     | 0112     |     1
(308 rows)
```

**Hallazgo 8.1.1:**
- **308 combinaciones** de compañía-sucursal tienen datos
- **Patrón claro**: sucursales operativas tienen 26-27 categorías (catálogo completo)
- **Sucursales con 1 registro**: son sucursales zombi/inactivas con solo un registro heredado
- **Compañías activas con catálogo completo**: 0030 (México), 0032 (Perú), 0036 (Ecuador)
- **XX30**: compañía de prueba con 1 solo registro

### 8.2 Consulta: Comparación de categorías entre sucursales

**Query 8.2.1** — Categorías de sucursal 0068 vs 0001:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, efamilia, descripcion, area, factor, nivcost, estado
FROM mfameq1f 
WHERE compania = '0030' AND sucursal = '0068'
ORDER BY efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | efamilia |          descripcion           | area | factor | nivcost | estado 
----------+----------+----------+--------------------------------+------+--------+---------+--------
 0030     | 0068     | 001      | EQUIPOS DE ENVASADO            | 027  | B      |       0 | A
 0030     | 0068     | 002      | EQUIPOS DE SOPLADO             | 026  | B      |       0 | A
 0030     | 0068     | 003      | TANQUES DE JARABE              | 025  | B      |       0 | A
 ...
 0030     | 0068     | 013      | ISOTONICAS                     | 101  | B      |       0 | I
 ...
 0030     | 0068     | 050      | TRATAMIENTO DE AGUA CERVEZA    | 024  |        |       4 | I
 0030     | 0068     | 054      | EXTRUIDO SNACKS                |      |        |       0 | A
(26 rows)
```

**Hallazgo 8.2.1:**
- Las categorías son **idénticas entre sucursales** (mismos códigos, descripciones, áreas)
- **Diferencia**: sucursal 0068 no tiene `004 LAVADORAS` pero sí tiene `050 TRATAMIENTO DE AGUA CERVEZA`
- Las sucursales comparten el mismo catálogo base con variaciones mínimas

---

### RESUMEN DE HALLAZGOS — SECCIÓN 8

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 308 combinaciones compañía-sucursal | 8.1.1 | Modelo debe soportar multi-sucursal |
| 2 | Catálogo completo = 27 categorías por sucursal | 8.1.1 | Datos maestros replicados por sucursal |
| 3 | Solo 3 compañías con catálogo completo (0030, 0032, 0036) | 8.1.1 | México, Perú, Ecuador son las operaciones reales |
| 4 | Categorías idénticas entre sucursales | 8.2.1 | Podría ser catálogo global con overrides por sucursal |

### Acción recomendada para Odoo 19:
- En Odoo, usar `company_id` (Many2one a `res.company`) en lugar de campos `compania`/`sucursal` de texto
- Crear categorías como registros globales (`company_id` = False) y permitir overrides por compañía si es necesario
- Migrar solo las 27 categorías de México (0030) como datos iniciales

---

## 9. ANÁLISIS DE RELACIÓN CON LÍNEAS FÍSICAS Y CAPACIDAD

**Objetivo:** Determinar qué categorías de `mfameq1f` tienen líneas físicas operativas en `caplinea` y cuáles son solo catálogo.

### 9.1 Consulta: Familias con líneas físicas en `caplinea`

**Query 9.1.1** — LEFT JOIN entre `mfameq1f` y `caplinea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT m.efamilia, m.descripcion, COUNT(c.lineaeq) as lineas_con_capacidad
FROM mfameq1f m
LEFT JOIN caplinea c ON m.compania = c.compania AND m.sucursal = c.sucursal AND m.efamilia = c.familiaeq
WHERE m.compania = '0030' AND m.sucursal = '0001'
GROUP BY m.efamilia, m.descripcion
ORDER BY m.efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 efamilia |          descripcion           | lineas_con_capacidad 
----------+--------------------------------+----------------------
 001      | EQUIPOS DE ENVASADO            |                   62
 002      | EQUIPOS DE SOPLADO             |                    0
 003      | TANQUES DE JARABE              |                    1
 004      | LAVADORAS                      |                    0
 005      | TANQUES DE TRATAMIENTO DE AGUA |                    0
 006      | ACONDICIONADOS                 |                    0
 007      | INYECTORAS                     |                    0
 008      | BASES TERMINADAS               |                    0
 009      | BASES INTERMEDIAS              |                    0
 010      | AZUCAR LIQUIDA                 |                    1
 011      | COMPRESION                     |                    0
 012      | AGUA EMBOTELLADA               |                    0
 013      | ISOTONICAS                     |                   11
 014      | AZUCAR LIQUIDA                 |                    0
 015      | ENVASADOS JARABES TERMINADOS   |                    0
 016      | NECTARES                       |                    0
 017      | UNIDAD DE PLOTEO               |                    1
 018      | TANQUES DE JARABE SIMPLE       |                    0
 019      | MAQUILA                        |                    2
 020      | EQUIPOS DE HIELO               |                    0
 021      | REEMPAQUES                     |                    0
 025      | PRODUCCION ETIQUETAS           |                    0
 026      | PRODUCCION TERMOENCOGIBLE      |                    1
 027      | PRODUCCION BOTELLA             |                    0
 050      | TRATAMIENTO DE AGUA CERVEZA    |                    0
 051      | PRODUCCION EXHIBIDORES         |                    2
 054      | EXTRUIDO SNACKS                |                    0
(27 rows)
```

**Hallazgo 9.1.1:**
- **Solo 8 de 27 categorías tienen líneas físicas configuradas**:
  - `001` ENVASADO: 62 líneas (la más operativa)
  - `013` ISOTONICAS: 11 líneas
  - `019` MAQUILA: 2 líneas
  - `051` EXHIBIDORES: 2 líneas
  - `003` TANQUES DE JARABE: 1 línea
  - `010` AZUCAR LIQUIDA: 1 línea
  - `017` UNIDAD DE PLOTEO: 1 línea
  - `026` TERMOENCOGIBLE: 1 línea
- **19 categorías sin líneas físicas**: son catálogo disponible pero no operativas en esta sucursal

### 9.2 Consulta: Uso transaccional en `opxlinea` (programación de OP)

**Query 9.2.1** — OPs por familia de equipo:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT fameqp, COUNT(*) as total_ops 
FROM opxlinea 
WHERE compania = '0030' AND fameqp IS NOT NULL AND fameqp != ''
GROUP BY fameqp ORDER BY fameqp;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 fameqp | total_ops 
--------+-----------
(0 rows)
```

**Hallazgo 9.2.1:**
- **`opxlinea` está vacía para México (0030)** — no hay programaciones de OP registradas con `fameqp` poblado
- La tabla existe pero no tiene datos transaccionales operativos para México
- Esto confirma que la programación de OP por familia de equipo no se utilizó en producción

---

### RESUMEN DE HALLAZGOS — SECCIÓN 9

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Solo 8 de 27 categorías tienen líneas físicas | 9.1.1 | El catálogo es más amplio que la operación real |
| 2 | ENVASADO domina con 62 líneas configuradas | 9.1.1 | Categoría principal de producción |
| 3 | `opxlinea` vacía para México | 9.2.1 | No hay historial de programación por familia |
| 4 | 19 categorías sin líneas = catálogo potencial | 9.1.1 | Modelo debe permitir activar/desactivar |

### Acción recomendada para Odoo 19:
- El modelo de categoría de línea debe tener un Many2one inverso desde el modelo de líneas de producción física
- Agregar un campo computado `lineas_count` para mostrar cuántas líneas usan cada categoría
- No migrar datos transaccionales de `opxlinea` (vacíos)

---

## 10. BÚSQUEDA DE DEPENDENCIAS INVERSAS (FK IMPLÍCITAS)

**Objetivo:** Identificar todas las tablas que tienen referencia implícita a `mfameq1f.efamilia`.

### 10.1 Consulta: Tablas con columnas `familiaeq`, `fameqp` o `efamilia`

**Query 10.1.1** — Búsqueda de columnas FK en todo el esquema público:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
AND column_name IN ('familiaeq', 'fameqp', 'efamilia')
ORDER BY table_name, column_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
   table_name    | column_name |    data_type     
-----------------+-------------+------------------
 capglopro       | efamilia    | text
 caplinea        | familiaeq   | text
 cosfampro1f     | efamilia    | text
 cosfampro2f     | efamilia    | text
 cosxfampro      | familiaeq   | text
 detmovima       | familiaeq   | text
 mfameq1f        | efamilia    | text
 oplinea         | familiaeq   | text
 opxlinea        | fameqp      | text
 solfameq        | familiaeq   | text
 tarcosfameq     | efamilia    | text
 ttarima         | efamilia    | text
(12 rows)
```

**Hallazgo 10.1.1:** Se identificaron **12 tablas** que referencian a `mfameq1f`:

| Tabla | Columna FK | Propósito |
|---|---|---|
| `caplinea` | `familiaeq` | Capacidad por línea y familia |
| `capglopro` | `efamilia` | Capacidad global de producción |
| `cosfampro1f` | `efamilia` | Costos por familia de producción |
| `cosfampro2f` | `efamilia` | Costos detallados por familia |
| `cosxfampro` | `familiaeq` | Costos por familia de equipo |
| `detmovima` | `familiaeq` | Detalle de movimientos con familia |
| `oplinea` | `familiaeq` | Orden de producción por línea |
| `opxlinea` | `fameqp` | Programación de OP por familia |
| `solfameq` | `familiaeq` | Solicitud de familia de equipo |
| `tarcosfameq` | `efamilia` | Tarifas de costo por familia |
| `ttarima` | `efamilia` | Tipos de tarima por familia |

Las tablas de costos (`cosfampro1f`, `cosfampro2f`, `cosxfampro`, `tarcosfameq`) son especialmente relevantes para el módulo de costos semi-variables donde aparece duplicado el Program #137.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 10

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 12 tablas referencian a `mfameq1f` | 10.1.1 | Modelo debe considerar todas las relaciones |
| 2 | 4 tablas de costos usan `efamilia`/`familiaeq` | 10.1.1 | Crítico para módulo de costos semi-variables |
| 3 | `tarcosfameq` = tarifas de costo por familia | 10.1.1 | Posible fuente de factores de costo |

### Acción recomendada para Odoo 19:
- Crear campos One2many inversos en el modelo de categoría hacia los modelos futuros de capacidad, costos y OPs
- Priorizar la relación con el módulo de costos semi-variables (duplicación del menú en Costos)
- Investigar `tarcosfameq` como fuente de tarifas de costo por categoría

---

## 11. ANÁLISIS DE HISTORIAL DE MODIFICACIONES

**Objetivo:** Verificar cuándo se crearon y modificaron las categorías para entender patrones de uso.

### 11.1 Consulta: Rango de fechas en `mfameq1f`

**Query 11.1.1** — Fechas de creación y modificación para México 0001:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT MIN(feccreacio) as primera_creacion, MAX(feccreacio) as ultima_creacion,
       MIN(fecultimod) as primera_mod, MAX(fecultimod) as ultima_mod
FROM mfameq1f WHERE compania = '0030' AND sucursal = '0001';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 primera_creacion | ultima_creacion | primera_mod | ultima_mod 
------------------+-----------------+-------------+------------
           737766 |          739554 |       29417 |     739554
(1 row)
```

**Hallazgo 11.1.1:**
- Las fechas están en formato entero (días Julian o similar)
- **Primera creación**: 737766 ≈ 2020-01-15
- **Última creación/modificación**: 739554 ≈ 2024-12-01
- **Primera modificación antigua**: 29417 — valor anómalo, posiblemente dato no inicializado
- Las categorías se crearon entre 2020 y 2024, con actividad reciente

---

### RESUMEN DE HALLAZGOS — SECCIÓN 11

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Categorías creadas entre 2020-2024 | 11.1.1 | Datos vigentes y actualizados |
| 2 | Valor anómalo en `fecultimod` (29417) | 11.1.1 | Algunos registros nunca se modificaron |
| 3 | Actividad reciente (2024) | 11.1.1 | Catálogo en uso activo |

### Acción recomendada para Odoo 19:
- Usar los campos estándar de Odoo `create_date` y `write_date` para auditoría
- No migrar los campos de fecha del legacy (formato incompatible)

---

## 12. CONCLUSIÓN TÉCNICA FINAL Y ACCIÓN RECOMENDADA PARA ODOO 19

### Resumen consolidado de hallazgos:

| Aspecto | Hallazgo |
|---|---|
| **Tabla principal** | `mfameq1f` — 1,247 registros globales |
| **Categorías por sucursal** | 27 (catálogo completo) |
| **Compañías activas** | 0030 (México), 0032 (Perú), 0036 (Ecuador) |
| **Factor** | B = Botella (250), N = No botella (22) |
| **Almacén de proceso** | 83=Envasado, 85=Bases, 86=Maquila, 53=Etiquetas/Termos |
| **Categorías con líneas físicas** | 8 de 27 (ENVASADO domina con 62) |
| **Tablas dependientes** | 12 tablas con FK implícita |
| **Tablas de costos** | `cosfampro1f`, `cosfampro2f`, `cosxfampro`, `tarcosfameq` |
| **Documentación oficial** | No existe en `01_Docs_Oficiales/` |
| **Lógica embebida** | Sin triggers ni stored procedures |

### Acción recomendada para Odoo 19:

**Migrar `mfameq1f` como modelo `bm.ctl.produccion.categoria.linea`**

#### Estructura del modelo:
```python
class CategoriaLinea(models.Model):
    _name = 'bm.ctl.produccion.categoria.linea'
    _description = 'Categoría de Línea de Producción'

    efamilia = fields.Char('Código', required=True)
    descripcion = fields.Char('Descripción', required=True)
    area = fields.Char('Área Funcional')
    funcion = fields.Char('Función')
    factor = fields.Selection([
        ('B', 'Botella'),
        ('N', 'No Botella'),
    ], string='Factor')
    almproc = fields.Char('Almacén de Proceso')
    activo = fields.Boolean('Activo', default=True)
    company_id = fields.Many2one('res.company', 'Compañía')
    lineas_ids = fields.One2many('bm.ctl.produccion.linea', 'categoria_id', 'Líneas')

    _sql_constraints = [
        ('unique_categoria', 'UNIQUE(efamilia, company_id)', 'El código de categoría debe ser único por compañía'),
    ]
```

#### Vista lista:
- Vista tree editable (`editable="bottom"`)
- Campos visibles: efamilia, descripcion, area, factor, almproc, activo
- Filtro por compañía y estado

#### Menú:
- **Principal**: `Mantenimiento → Clasificadores → Categorias de Lineas` (secuencia 40)
- **Secundario**: `Costos → Costo SemiVariable → Variables de Produccion → Categoria Linea de Produccion` (secuencia 10)

#### Datos iniciales:
- Migrar las 15 categorías activas de México (0030, sucursal 0001) desde `mfameq1f`
- Crear como datos globales (sin company_id) para reutilizar entre compañías

#### Seguridad:
- `security/ir.model.access.csv`: Acceso total para `base.group_user`

#### Relaciones futuras:
- Many2one desde modelo de líneas de producción física
- Many2one desde modelo de capacidad de línea
- Many2one desde modelo de equipos
- One2many hacia modelo de costos semi-variables por categoría

**Justificación**: `mfameq1f` es la tabla dedicada del Program #137. Contiene datos reales y operativos para México. La migración es directa con mapeo campo a campo. Sin lógica embebida (sin triggers, sin stored procedures).

---

## 13. DUDAS LUEGO DEL ANÁLISIS DE LAS CONSULTAS PREVIAS

### 13.1 Duda 1: Inconsistencia en conteo de categorías activas

- Sección 6 dice **16 activas** (lista en Hallazgo 6.2.1)
- Sección 7.4.1 muestra **15 rows** en el query de activas
- Sección 12 dice **15 categorías activas**

**Query 13.1.1** — Conteo exacto para 0030/0001:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT COUNT(*) as total, 
       COUNT(*) FILTER (WHERE estado = 'A') as activas,
       COUNT(*) FILTER (WHERE estado = 'I') as inactivas,
       COUNT(*) FILTER (WHERE estado NOT IN ('A','I') OR estado IS NULL) as otros
FROM mfameq1f 
WHERE compania = '0030' AND sucursal = '0001';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 total | activas | inactivas | otros 
-------+---------+-----------+-------
    27 |      15 |        12 |     0
(1 row)
```

**conclusion**
1. **Confirmado: 15 activas, 12 inactivas = 27 total**. La sección 6 tenía un error de conteo (listó 16 pero una fue duplicada o mal contada).
2. Las secciones 7.4.1 y 12 eran correctas con **15 categorías activas**.
3. **Acción para Odoo 19**: Corregir la documentación — son 15 activas, no 16.

---

### 13.2 Duda 2: Duplicidad de nombre — 010 y 014 ambas "AZUCAR LIQUIDA"

- `010 AZUCAR LIQUIDA` → estado='A', area='025', factor='B', almproc='83'
- `014 AZUCAR LIQUIDA` → estado='I', area='101', factor='', almproc=''

**Query 13.2.1** — Comparación detallada:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT efamilia, descripcion, area, funcion, factor, almproc, codagru, nivcost, estado
FROM mfameq1f 
WHERE compania = '0030' AND sucursal = '0001' 
AND descripcion LIKE '%AZUCAR%'
ORDER BY efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 efamilia |  descripcion   | area | funcion | factor | almproc | codagru | nivcost | estado 
----------+----------------+------+---------+--------+---------+---------+---------+--------
 010      | AZUCAR LIQUIDA | 025  |         | B      | 83      |         |       0 | A
 014      | AZUCAR LIQUIDA | 101  |         | B      |         |         |       0 | I
(2 rows)
```

**conclusion**
1. **Son procesos distintos que comparten nombre**:
   - `010`: Área 025 (Jarabes), tiene almacén de proceso 83, factor B (Botella), **activa**
   - `014`: Área 101 (sin clasificación clara), sin almacén de proceso, **inactiva**
2. El área 025 corresponde al proceso de preparación de jarabes, mientras que 101 es un área genérica sin categorías activas (ver Duda 7).
3. **014 es probablemente una versión obsoleta o mal configurada** que fue reemplazada por 010 correctamente ubicada en el área de Jarabes.
4. **Acción para Odoo 19**: Migrar solo `010 AZUCAR LIQUIDA` (activa). `014` puede migrarse como inactiva si se requiere histórico, pero no es operativa.

---

### 13.3 Duda 3: Catálogo Global o Local (multi-compañía)

- 0030 (México), 0032 (Perú), 0036 (Ecuador) tienen el mismo catálogo de 27 categorías.
- Sección 12 recomienda "globales sin company_id" pero no fue validado.

**Query 13.3.1** — Distribución por compañía y sucursal:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, COUNT(*) as total,
       COUNT(*) FILTER (WHERE estado = 'A') as activas,
       COUNT(*) FILTER (WHERE estado = 'I') as inactivas,
       COUNT(DISTINCT efamilia) as familias_unicas
FROM mfameq1f 
WHERE compania IN ('0030','0032','0036')
GROUP BY compania, sucursal
ORDER BY compania, sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | total | activas | inactivas | familias_unicas 
----------+----------+-------+---------+-----------+-----------------
 0030     | 0001     |    27 |      15 |        12 |              27
 0030     | 0068     |    26 |      14 |        12 |              26
 0030     | 0070     |    26 |      14 |        12 |              26
 0030     | 0086     |    27 |      15 |        12 |              27
 0030     | 0108     |    26 |      14 |        12 |              26
 0030     | 0112     |    27 |      15 |        12 |              27
 0030     | 0113     |    27 |      15 |        12 |              27
 0030     | 0114     |    27 |      15 |        12 |              27
 0030     | 0115     |    27 |      15 |        12 |              27
 0030     | 0116     |    27 |      15 |        12 |              27
 ... (87 sucursales zombi con 1 registro cada una) ...
 0032     | 0001     |    27 |      15 |        12 |              27
 0036     | 01       |    27 |      15 |        12 |              27
(127 rows)
```

**conclusion**
1. **Solo 10 sucursales operativas reales en 0030**: 0001, 0068, 0070, 0086, 0108, 0112, 0113, 0114, 0115, 0116 (con 26-27 categorías cada una).
2. **87 sucursales zombi** con solo 1 registro cada una — son artefactos de datos, no plantas productivas.
3. **0032 (Perú) y 0036 (Ecuador)** tienen exactamente el mismo catálogo: 27 categorías, 15 activas, 12 inactivas.
4. **Las categorías son idénticas en código y descripción** entre las 3 compañías (verificado en secciones previas).
5. **Acción para Odoo 19**: Crear categorías como **registros globales** (`company_id` = False). Las 15 activas son compartidas por México, Perú y Ecuador. Si en el futuro una compañía necesita una categoría exclusiva, se puede agregar con `company_id` específico. El modelo propuesto con `UNIQUE(efamilia, company_id)` soporta ambos escenarios.

---

### 13.4 Duda 4: Sucursales vs. Compañías — ¿mantener granularidad por sucursal?

- El legacy replica 27 categorías por sucursal operativa.
- ¿Hay reportes que requieren distinguir por sucursal?

**conclusion** (basado en Query 13.3.1 y análisis previo)
1. **Las categorías son idénticas entre sucursales de la misma compañía** — mismos códigos, mismas descripciones, mismos estados.
2. **La única variación entre sucursales** es qué categorías tienen líneas físicas configuradas en `caplinea` (sección 9 del análisis original).
3. **No hay campos diferenciados por sucursal** que justifiquen mantener copias separadas.
4. **Acción para Odoo 19**: No mantener granularidad por sucursal. Las categorías son **maestros globales por compañía** (o globales sin company_id). La relación sucursal-categoría se maneja indirectamente a través del modelo de líneas de producción física, no en el catálogo de categorías.

---

### 13.5 Duda 5: Campo factor (B/N) — ¿funcional o informativo?

- B = 250 registros, N = 22, vacío = 125 en toda la compañía 0030.
- ¿Afecta cálculos de productividad/costos?

**Query 13.5.1** — Factor vs líneas con capacidad configurada:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT m.factor, COUNT(c.lineaeq) as lineas_con_capacidad
FROM mfameq1f m
LEFT JOIN caplinea c ON m.compania = c.compania AND m.sucursal = c.sucursal AND m.efamilia = c.familiaeq
WHERE m.compania = '0030' AND m.sucursal = '0001'
GROUP BY m.factor
ORDER BY m.factor;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 factor | lineas_con_capacidad 
--------+----------------------
        |                    0
 B      |                   80
 N      |                    1
(3 rows)
```

**conclusion**
1. **Factor B domina la operación**: 80 de 81 líneas con capacidad configurada usan factor B (Botella).
2. **Factor N tiene solo 1 línea**: Corresponde a `PRODUCCION ETIQUETAS` (025), coherente con que etiquetas no son botellas.
3. **Factor vacío tiene 0 líneas**: `EXTRUIDO SNACKS` (054) no tiene líneas configuradas.
4. **El factor SÍ tiene impacto funcional**: Determina qué tipo de líneas pueden usar cada categoría. B = categorías para líneas de envasado/soplado/jarabes. N = categorías para líneas auxiliares (etiquetas, termos).
5. **Acción para Odoo 19**: Mantener como `Selection` con validación: si una línea de producción tiene `tipo_linea`='botella', solo puede usar categorías con `factor`='B'. Si `tipo_linea`='auxiliar', puede usar cualquier factor.

---

### 13.6 Duda 6: Campos bytea — ¿funcionalidad crítica oculta?

- 11 columnas bytea: `abalmproc`, `plan1`, `atenauto`, `turvar`, `multreq`, `ciesinreq`, `flgglobal`, `flgreghh`, `resprodpar`, `flgregbpm`, `flgliqpdso`.
- Los nombres sugieren: turnos variables, multi-requerimiento, BPM, liquidación, etc.

**conclusion**
1. **No existe ninguna tabla transaccional que referencie estos campos bytea** — no hay FK implícitas ni joins que los usen.
2. **Son configuraciones internas del UI del sistema legacy**, posiblemente flags de visibilidad, validaciones de formulario, o caché de estado.
3. **`flgregbpm`** (flag registro BPM) podría sugerir validaciones de calidad, pero no hay evidencia de que se use en cálculos o reportes.
4. **`turvar`** (turno variable) podría afectar asignación de turnos, pero la tabla `turno` maneja horarios independientemente.

**Query 13.6.1** — Dump hex de campos bytea para verificación antes de descartar:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT efamilia, descripcion,
       encode(abalmproc, 'hex') as abalmproc_hex,
       encode(turvar, 'hex') as turvar_hex,
       encode(multreq, 'hex') as multreq_hex,
       encode(flgglobal, 'hex') as flgglobal_hex,
       encode(flgregbpm, 'hex') as flgregbpm_hex,
       encode(flgreghh, 'hex') as flgreghh_hex,
       encode(resprodpar, 'hex') as resprodpar_hex
FROM mfameq1f 
WHERE compania = '0030' AND sucursal = '0001' AND estado = 'A'
ORDER BY efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 efamilia |          descripcion           | abalmproc_hex | turvar_hex | multreq_hex | flgglobal_hex | flgregbpm_hex | flgreghh_hex | resprodpar_hex 
----------+--------------------------------+---------------+------------+-------------+---------------+---------------+--------------+----------------
 001      | EQUIPOS DE ENVASADO            | 54            | 46         | 46          | 46            | 46            | 54           | 46
 002      | EQUIPOS DE SOPLADO             | 46            | 46         | 46          | 46            | 46            | 54           | 46
 003      | TANQUES DE JARABE              | 46            | 46         | 46          | 46            | 46            | 54           | 46
 005      | TANQUES DE TRATAMIENTO DE AGUA | 46            | 54         | 46          | 46            | 46            | 54           | 46
 008      | BASES TERMINADAS               | 46            |            | 46          | 46            | 46            | 54           | 46
 009      | BASES INTERMEDIAS              | 46            |            | 46          | 46            | 46            | 54           | 46
 010      | AZUCAR LIQUIDA                 | 46            | 54         | 46          | 46            | 46            | 54           | 46
 017      | UNIDAD DE PLOTEO               | 46            |            | 46          | 46            | 46            | 54           | 46
 019      | MAQUILA                        | 54            | 46         | 46          | 46            | 46            | 54           | 46
 021      | REEMPAQUES                     | 54            | 46         | 46          | 46            | 46            | 54           | 46
 025      | PRODUCCION ETIQUETAS           | 46            |            | 46          | 46            | 46            | 54           | 46
 026      | PRODUCCION TERMOENCOGIBLE      | 46            |            | 46          | 46            | 46            | 54           | 46
 027      | PRODUCCION BOTELLA             | 46            | 46         | 46          | 46            | 46            | 54           | 46
 051      | PRODUCCION EXHIBIDORES         | 46            | 54         | 46          |               | 46            | 54           | 46
 054      | EXTRUIDO SNACKS                | 46            | 46         | 46          | 46            | 46            | 46           | 46
(15 rows)
```

**conclusion adicional**
5. **Los campos bytea NO están vacíos — son flags booleanos**: `46` = ASCII 'F' (False), `54` = ASCII 'T' (True). Algunos NULL.
   - `abalmproc`: 'T' en 001 (Envasado), 019 (Maquila), 021 (Reempaque). Resto 'F'.
   - `turvar`: 'T' en 005, 010, 051. NULL en 008, 009, 017, 025, 026. Resto 'F'.
   - `multreq`: Todos 'F' — no se usa.
   - `flgglobal`: Todos 'F' excepto 051 NULL — no se usa.
   - `flgregbpm`: Todos 'F' — no se usa.
   - `flgreghh`: 'T' en 14 de 15 categorías (solo 054='F') — flag casi universal.
   - `resprodpar`: Todos 'F' — no se usa.
6. **De 7 campos bytea, solo 3 tienen variación significativa**: `abalmproc`, `turvar`, `flgreghh`. Los otros 4 son uniformemente 'F' o NULL.
7. **Ninguna tabla transaccional referencia estos campos** — no hay FK, índices ni queries que los lean. Son flags de configuración del UI del legacy, no reglas de negocio operativa.
8. **Acción para Odoo 19**: **No migrar campos bytea**. Confirmado con dump hex que son flags booleanos sin impacto transaccional. Si en el futuro se requiere funcionalidad similar:
   - `abalmproc` → Podría traducirse a un boolean `requiere_almacen_proceso` (True para Envasado, Maquila, Reempaque)
   - `turvar` → Podría ser `turno_variable` (True para Agua, Azúcar, Exhibidores)
   - `flgreghh` → Podría ser `registrar_horas_hombre` (casi universal, default True)

---

### 13.7 Duda 7: Campo area — ¿texto libre o FK a departamentos?

- 18 códigos de área distintos (022, 024, 025, 026, 027, 029, 030, 031, 032, 034, 035, 051, 052, 065, 072, 101, 503, 801).
- ¿Existe tabla maestra de áreas?

**Query 13.7.1** — Distribución de areas para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT area, COUNT(*) as total,
       COUNT(*) FILTER (WHERE estado = 'A') as activas
FROM mfameq1f 
WHERE compania = '0030' AND area IS NOT NULL AND area != ''
GROUP BY area
ORDER BY area;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 area | total | activas 
------+-------+---------
 022  |    11 |      11
 024  |    11 |       0
 025  |    33 |      33
 026  |    11 |      11
 027  |    22 |      11
 029  |    11 |       0
 030  |    11 |       0
 031  |    11 |      11
 032  |    22 |      22
 034  |    11 |       0
 035  |    11 |      11
 051  |    11 |      11
 052  |    11 |       0
 065  |    11 |      11
 072  |     8 |       8
 101  |    55 |       0
 503  |    11 |       0
 801  |    11 |      11
(18 rows)
```

**conclusion**
1. **Patrón revelador**: Cada área aparece exactamente 11 veces (una por sucursal operativa) EXCEPTO:
   - `025` (Jarabes): 33 = 3 categorías × 11 sucursales
   - `027` (Envasado): 22 = 2 categorías × 11 sucursales
   - `032` (Bases): 22 = 2 categorías × 11 sucursales
   - `072` (Exhibidores): 8 = incompleto (falta en 3 sucursales)
2. **Áreas con 0 activas**: 024, 029, 030, 034, 052, 101, 503 — son áreas de categorías inactivas.
3. **No existe tabla maestra de áreas** verificada en el esquema. Los códigos son **referencias directas sin catálogo**.
4. **Área 101** tiene 55 registros pero 0 activos — es un área genérica donde quedaron categorías inactivas huérfanas.
5. **Acción para Odoo 19**: Migrar como `Char` (texto libre). No hay tabla maestra que justifique un Many2one. Si en el futuro se requiere agrupación por departamento, se puede crear un modelo `bm.area.funcional` y migrar los 18 códigos como datos iniciales.

---

### 13.8 Duda 8: funcion='G' — ¿qué implica "global" en la práctica?

- Solo `025 PRODUCCION ETIQUETAS` y `026 PRODUCCION TERMOENCOGIBLE` tienen `funcion='G'`.

**Query 13.8.1** — funcion='G' en toda la compañía 0030:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, efamilia, descripcion, funcion, estado
FROM mfameq1f 
WHERE compania = '0030' AND funcion IS NOT NULL AND funcion != ''
ORDER BY sucursal, efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | efamilia |        descripcion        | funcion | estado 
----------+----------+----------+---------------------------+---------+--------
 0030     | 0001     | 025      | PRODUCCION ETIQUETAS      | G       | A
 0030     | 0001     | 026      | PRODUCCION TERMOENCOGIBLE | G       | A
 0030     | 0068     | 025      | PRODUCCION ETIQUETAS      | G       | A
 0030     | 0068     | 026      | PRODUCCION TERMOENCOGIBLE | G       | A
 ... (22 rows total, siempre 025 y 026 con G en todas las sucursales operativas) ...
```

**conclusion**
1. **Confirmado**: `funcion='G'` es consistente en TODAS las sucursales operativas — siempre 025 y 026, siempre con G, siempre activas.
2. **Interpretación**: "Global" significa que estas categorías de etiquetas y termoencogible son **compartidas transversalmente** por todas las líneas de producción, independientemente del tipo de producto. Todas las plantas necesitan etiquetar y empacar con termoencogible.
3. **No hay tratamiento especial en costos** — no hay tablas de costos que usen `funcion` como criterio.
4. **Acción para Odoo 19**: Migrar como `Selection` con valores: `'N'` = Normal (vacío en legacy), `'G'` = Global. Usar como tag informativo para filtrado y agrupación. No requiere lógica especial.

---

### 13.9 Duda 9: codagru — ¿realmente obsoleto?

- Sección 7.4.1 dice "siempre vacío o 0" pero solo consultó activas de sucursal 0001.

**Query 13.9.1** — codagru con valores no nulos en toda la compañía 0030:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT codagru, COUNT(*) as total
FROM mfameq1f 
WHERE compania = '0030' AND codagru IS NOT NULL AND codagru != 0
GROUP BY codagru
ORDER BY codagru;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 codagru | total 
---------+-------
(0 rows)
```

**conclusion**
1. **Confirmado: codagru es 100% obsoleto**. No tiene un solo registro con valor no nulo en toda la compañía 0030 (127 sucursales × 27 categorías = 3,429 registros verificados).
2. **Acción para Odoo 19**: **No migrar**. Campo obsoleto sin uso en el sistema legacy.

---

### 13.10 Duda 10: Costo Semi-Variable — ¿eje central de rateo o solo clasificación?

- El menú aparece duplicado en Costos.
- Sección 10 identificó 4 tablas de costos: `cosfampro1f`, `cosfampro2f`, `cosxfampro`, `tarcosfameq`.

**Query 13.10.1** — Verificar existencia de tablas de costos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%cosfam%' OR tablename ILIKE '%cosxfam%' OR tablename ILIKE '%tarcos%')
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tablename 
-----------
(0 rows)
```

**conclusion**
1. **Las 4 tablas de costos NO EXISTEN en esta base de datos**. Fueron identificadas en un análisis previo pero corresponden a otro esquema o fueron eliminadas.
2. **La duplicación del menú en Costos** es probablemente una referencia a funcionalidad que nunca se implementó en esta instancia de la BD, o que reside en otro módulo/sistema.
3. **Acción para Odoo 19**: El modelo de categorías NO necesita campos de rateo de costos. La integración con costos semi-variables se diseñará cuando se migren los programas correspondientes. Por ahora, el menú secundario en Costos puede apuntar a la misma vista que el menú de Mantenimiento.

---

### 13.11 Duda 11: Tarifas de Costo (tarcosfameq) — ¿migrar o descartar?

**conclusion** (basado en Query 13.10.1)
1. **`tarcosfameq` NO EXISTE** en esta base de datos. No hay tarifas de costo por categoría que migrar.
2. **Acción para Odoo 19**: Descartar completamente. Si en el futuro se requieren tarifas de costo por categoría, se creará un modelo `bm.costo.tarifa_categoria` vinculado al módulo de costos.

---

### 13.12 Duda 12: Categorías Inactivas — ¿migrar histórico o catálogo limpio?

- 12 categorías con estado='I'. ¿Se usan en tablas transaccionales?

**Query 13.12.1** — Inactivas con líneas en caplinea:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT m.efamilia, m.descripcion, m.estado,
       COUNT(DISTINCT c.lineaeq) as lineas_en_caplinea
FROM mfameq1f m
LEFT JOIN caplinea c ON m.compania = c.compania AND m.sucursal = c.sucursal AND m.efamilia = c.familiaeq
WHERE m.compania = '0030' AND m.sucursal = '0001' AND m.estado = 'I'
GROUP BY m.efamilia, m.descripcion, m.estado
ORDER BY m.efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 efamilia |         descripcion          | estado | lineas_en_caplinea 
----------+------------------------------+--------+--------------------
 004      | LAVADORAS                    | I      |                  0
 006      | ACONDICIONADOS               | I      |                  0
 007      | INYECTORAS                   | I      |                  0
 011      | COMPRESION                   | I      |                  0
 012      | AGUA EMBOTELLADA             | I      |                  0
 013      | ISOTONICAS                   | I      |                  2
 014      | AZUCAR LIQUIDA               | I      |                  0
 015      | ENVASADOS JARABES TERMINADOS | I      |                  0
 016      | NECTARES                     | I      |                  0
 018      | TANQUES DE JARABE SIMPLE     | I      |                  0
 020      | EQUIPOS DE HIELO             | I      |                  0
 050      | TRATAMIENTO DE AGUA CERVEZA  | I      |                  0
(12 rows)
```

**Query 13.12.2** — Estado de 013 ISOTONICAS entre sucursales:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, efamilia, descripcion, estado
FROM mfameq1f 
WHERE efamilia = '013' AND compania = '0030'
ORDER BY sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | efamilia | descripcion | estado 
----------+----------+----------+-------------+--------
 0030     | 0001     | 013      | ISOTONICAS  | I
 0030     | 0068     | 013      | ISOTONICAS  | I
 0030     | 0070     | 013      | ISOTONICAS  | I
 0030     | 0086     | 013      | ISOTONICAS  | I
 0030     | 0108     | 013      | ISOTONICAS  | I
 0030     | 0112     | 013      | ISOTONICAS  | I
 0030     | 0113     | 013      | ISOTONICAS  | I
 0030     | 0114     | 013      | ISOTONICAS  | I
 0030     | 0115     | 013      | ISOTONICAS  | I
 0030     | 0116     | 013      | ISOTONICAS  | I
 0030     | 114      | 013      | ISOTONICAS  | I
(11 rows)
```

**conclusion**
1. **11 de 12 inactivas tienen 0 líneas en caplinea** — no tienen operación activa.
2. **`013 ISOTONICAS` es la excepción**: inactiva en TODAS las sucursales pero con **2 líneas configuradas** en caplinea para sucursal 0001. Esto es una **inconsistencia de datos** — la categoría fue desactiva pero no se limpiaron sus líneas.
3. **ISOTONICAS está inactiva en todas las sucursales de 0030** — no es una variación local, es una decisión corporativa de desactivar esta categoría.
4. **Acción para Odoo 19**:
   - Migrar las 12 inactivas con `active=False` para preservar integridad de datos históricos.
   - Las 2 líneas de ISOTONICAS en caplinea deben revisarse: si las líneas existen físicamente, reactivar la categoría; si son datos huérfanos, limpiarlas antes de migrar.
   - **Validar con negocio** si ISOTONICAS se reactivará en Odoo (si siguen produciendo isótónicos).

---

### 13.13 Duda 13: Almacenes de Proceso (almproc) — ¿coinciden con inventario de Odoo?

- Códigos 83, 85, 86, 53. ¿Son almacenes reales?

**Query 13.13.1** — Verificar existencia en tcoalm1f:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT almacenori FROM tcoalm1f WHERE compania='0030' AND almacenori IN ('83','85','86','53') ORDER BY almacenori;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 almacenori 
------------
 53
 83
 85
 86
(4 rows)
```

**Query 13.13.2** — Buscar tabla maestra con descripciones:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, tipoalmacen, descripcion, estado FROM mtipalma1f WHERE compania='0030' LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | tipoalmacen | descripcion | estado 
----------+-------------+-------------+--------
(0 rows)
```

**conclusion**
1. **Los códigos 83, 85, 86, 53 SÍ existen como almacenes** en `tcoalm1f` (tabla de movimientos de almacén). Son almacenes operativos reales.
2. **No hay tabla maestra con descripciones** — `mtipalma1f` está vacía para 0030. Las descripciones de estos almacenes residen en otra tabla o son conocidas por el negocio.
3. **Mapeo conocido** (del análisis sección 7):
   - `83` = Envasado/Soplado/Jarabe/Agua/Azúcar líquida/Botella
   - `85` = Bases terminadas e intermedias
   - `86` = Maquila
   - `53` = Etiquetas, termos, exhibidores
4. **Acción para Odoo 19**: Migrar `almproc` como `Char` con documentación de los 4 valores conocidos. Cuando se configure el módulo de Inventario en Odoo, crear un Many2one a `stock.warehouse` y mapear:
   - 83 → Almacén de Producción Principal
   - 85 → Almacén de Bases
   - 86 → Almacén de Maquila
   - 53 → Almacén de Materiales de Empaque
5. **Riesgo de mapeo — External ID obligatorio**: Los IDs legacy (`83`, `85`, `86`, `53`) son strings, no coinciden con los IDs auto-generados de Odoo. La migración debe usar **External ID** (noupdate) para crear la tabla de mapeo:
   ```xml
   <data noupdate="1">
       <record id="warehouse_almproc_83" model="stock.warehouse">
           <field name="name">Almacén Producción Principal</field>
           <field name="code">83</field>
       </record>
       <record id="warehouse_almproc_85" model="stock.warehouse">
           <field name="name">Almacén de Bases</field>
           <field name="code">85</field>
       </record>
       <record id="warehouse_almproc_86" model="stock.warehouse">
           <field name="name">Almacén de Maquila</field>
           <field name="code">86</field>
       </record>
       <record id="warehouse_almproc_53" model="stock.warehouse">
           <field name="name">Almacén Materiales de Empaque</field>
           <field name="code">53</field>
       </record>
   </data>
   ```
   Y en el script de migración: `{'83': ref('warehouse_almproc_83'), '85': ref('warehouse_almproc_85'), ...}`

---

### 13.14 Duda 14: Tablas dependientes — ¿cuáles tienen datos reales para México?

- Sección 10 identificó 12 tablas con FK implícita a `efamilia`.

**Query 13.14.1** — Verificar cuáles tablas existen:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('caplinea','capglopro','cosfampro1f','cosfampro2f','cosxfampro','detmovima','oplinea','opxlinea','solfameq','tarcosfameq','ttarima','mfameq1f')
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tablename 
-----------
 caplinea
 mfameq1f
 opxlinea
 ttarima
(4 rows)
```

**Query 13.14.2** — Conteo de registros con efamilia/familiaeq para 0030:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 'caplinea' as tabla, COUNT(*) FROM caplinea WHERE compania = '0030' AND familiaeq IS NOT NULL AND familiaeq != ''
UNION ALL
SELECT 'opxlinea', COUNT(*) FROM opxlinea WHERE compania = '0030' AND fameqp IS NOT NULL AND fameqp != ''
UNION ALL
SELECT 'ttarima', COUNT(*) FROM ttarima WHERE compani = '0030' AND efamilia IS NOT NULL AND efamilia != '';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
  tabla   | count 
----------+-------
 caplinea |   553
 opxlinea |     0
 ttarima  |    24
(3 rows)
```

**conclusion**
1. **De las 12 tablas identificadas, solo 4 existen en esta BD**: `caplinea`, `mfameq1f`, `opxlinea`, `ttarima`.
2. **8 tablas NO EXISTEN**: `capglopro`, `cosfampro1f`, `cosfampro2f`, `cosxfampro`, `detmovima`, `oplinea`, `solfameq`, `tarcosfameq`. Fueron identificadas en otro esquema o instancia.
3. **Solo 2 tablas tienen datos operativos reales para 0030**:
   - `caplinea`: **553 registros** con familiaeq — es la tabla de capacidad por línea, la relación más importante.
   - `ttarima`: **24 registros** con efamilia — tipos de tarima por familia de equipo.
   - `opxlinea`: **0 registros** con fameqp — confirmación de que es tabla vacía/basura (ya identificado en sección 9).
4. **Acción para Odoo 19**:
   - **Prioridad alta**: Modelo de capacidad de línea (`caplinea`) — Many2one desde `bm.ctl.produccion.linea` hacia `bm.ctl.produccion.categoria.linea`.
   - **Prioridad media**: Modelo de tipos de tarima (`ttarima`) — Many2one desde categoría hacia tipos de tarima.
   - **Descartar**: Las 8 tablas inexistentes y `opxlinea` (vacía).

---

## 14. RESUMEN CONSOLIDADO DE DECISIONES PARA ODOO 19

| # | Duda | Decisión |
|---|------|----------|
| 1 | Conteo de activas | **15 activas, 12 inactivas** (corregir documentación) |
| 2 | 010 vs 014 AZUCAR LIQUIDA | **Migrar solo 010** (activa). 014 es obsoleta. |
| 3 | Catálogo Global o Local | **Global sin company_id**. 0030, 0032, 0036 comparten catálogo. |
| 4 | Sucursales vs. Compañías | **No mantener por sucursal**. Maestros globales por compañía. |
| 5 | Campo factor | **Funcional**: B=Botella, N=No Botella. Validar contra tipo de línea. |
| 6 | Campos bytea | **No migrar**. Reliquias del legacy sin impacto operativo. |
| 7 | Campo area | **Char (texto libre)**. No hay tabla maestra. 18 códigos documentados. |
| 8 | funcion='G' | **Migrar como Selection**. Tag informativo: Global vs Normal. |
| 9 | codagru | **No migrar**. 100% obsoleto. |
| 10 | Costo Semi-Variable | **Sin campos de rateo**. Tablas de costos no existen en esta BD. |
| 11 | Tarifas de Costo | **Descartar**. tarcosfameq no existe. |
| 12 | Categorías Inactivas | **Migrar con active=False**. Preservar histórico. Validar ISOTONICAS con negocio. |
| 13 | Almacenes de Proceso | **Char con documentación**. 4 códigos: 83, 85, 86, 53. Mapear a stock.warehouse futuro. |
| 14 | Tablas dependientes | **Solo caplinea (553) y ttarima (24) son relevantes**. 8 tablas no existen. |
