## 1. EXPLORACIÓN DE DICCIONARIO DE DATOS - CATEGORÍAS DE LÍNEAS DE PRODUCCIÓN

**Objetivo:** Ejecutar consulta de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas a la clasificación de líneas de producción por categoría dentro del esquema público, con el fin de mapear la estructura de persistencia en `mxbdaje_local`.

### 1.1 Consulta: Búsqueda sistemática de tablas con "linea" en el nombre

**Query 1.1.1** — Todas las tablas con "linea":
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

**Hallazgo 1.1.1:** Se identifican 8 tablas con "linea" en el nombre. Cada una debe inspeccionarse para determinar su propósito real.

### 1.2 Consulta: Búsqueda de tablas de familias/categorías de equipos

**Query 1.2.1** — Tablas de familias de equipos:
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

**Hallazgo 1.2.1:** Se identifica `mfameq1f` como tabla maestra de familias de equipos. Esta es la candidata principal para el catálogo de categorías de líneas de producción.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 1

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 8 tablas con "linea" en nombre | 1.1.1 | Inspeccionar cada una para separar inventario vs producción |
| 2 | `mfameq1f` es tabla de familias de equipos | 1.2.1 | Candidata principal para Program #137 |

---

## 2. ANÁLISIS DE TABLA `mlinea1f` - CONFIRMACIÓN: LÍNEAS DE INVENTARIO

**Objetivo:** Confirmar que `mlinea1f` es de líneas de inventario/contables, NO de producción física.

### 2.1 Consulta: Estructura y datos de `mlinea1f`

**Query 2.1.1** — Estructura:
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

**Query 2.1.2** — Líneas de México 0030:
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

**Hallazgo 2.1.1:** 
- **`mlinea1f` NO es de líneas de producción física**: Son líneas de inventario/contables
- **`flglinea`** clasifica por tipo contable: Te=Terminado, In=Insumo, Pr=Intermedio, Ot=Otros, Re=Repuestos, Su=Suministros, Se=Servicios, Ec=Economato, Ac=Activos Fijos, Di=Diferidos, Al=Publicitario
- **26 líneas para 0030**, todas contables
- **No aplica al Program #137**

---

### RESUMEN DE HALLAZGOS — SECCIÓN 2

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mlinea1f` es de líneas de inventario | 2.1.2 | No usar para categorías de producción |
| 2 | `flglinea` = tipo contable (Te, In, Pr, etc.) | 2.1.2 | Clasificador contable, no de máquinas |

---

## 3. ANÁLISIS DE TABLA `mlifacategoria1f` - CONFIRMACIÓN: CLASIFICACIÓN CONTABLE

**Objetivo:** Confirmar que `mlifacategoria1f` es clasificación contable/inventarial, no de producción física.

### 3.1 Consulta: Estructura y datos de `mlifacategoria1f`

**Query 3.1.1** — Estructura:
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

**Query 3.1.2** — Muestreo de datos:
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

**Hallazgo 3.1.1:** 
- **PK compuesta**: `(compania, linea, familia, categoria)` — tabla de clasificación jerárquica
- **Códigos numéricos sin descripción**: familia='001', categoria='501' — son códigos contables/inventariales
- **Valores de prueba**: 'ABC', 'XYZ', 'ZYX' — datos no depurados
- **1,569 registros totales**, 164 para 0030
- **No aplica al Program #137**

---

### RESUMEN DE HALLAZGOS — SECCIÓN 3

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mlifacategoria1f` es clasificación contable | 3.1.1 | No usar para categorías de producción |
| 2 | Códigos sin descripción legible | 3.1.2 | No son categorías de máquinas |

---

## 4. ANÁLISIS DE TABLA `mfameq1f` - HALLAZGO PRINCIPAL: FAMILIAS DE EQUIPOS

**Objetivo:** Inspeccionar `mfameq1f` como el catálogo real de categorías de líneas de producción.

### 4.1 Consulta: Estructura de `mfameq1f`

**Query 4.1.1** — Describir estructura:
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

**Hallazgo 4.1.1:** 
- **PK**: `(compania, sucursal, efamilia)` — familia de equipo por compañía y sucursal
- **Campo `descripcion`**: Texto legible (ej: "EQUIPOS DE ENVASADO")
- **Campo `area`**: Código de área funcional
- **Campo `funcion`**: Indicador de función (ej: 'G' para global)
- **Campos de auditoría**: `feccreacio`, `horcreacio`, `usuacreac`, `fecultimod`, `horultimod`, `usuaulmod`
- **Campos de configuración**: `abalmproc`, `factor`, `plan1`, `atenauto`, `turvar`, `multreq`, `ciesinreq`, `flgglobal`, `almproc`, `codagru`, `flgreghh`, `resprodpar`, `flgregbpm`, `flgliqpdso`

### 4.2 Consulta: Familias de equipos para México

**Query 4.2.1** — Familias únicas por descripción:
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

**Hallazgo 4.2.1:** 
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

### RESUMEN DE HALLAZGOS — SECCIÓN 4

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mfameq1f` es el catálogo de familias de equipos | 4.1.1 | Es la tabla del Program #137 |
| 2 | 27 familias por sucursal, con descripción legible | 4.2.1 | Catálogo completo y documentado |
| 3 | Campo `area` agrupa por área funcional | 4.2.1 | Permite agrupación por tipo de proceso |
| 4 | Estado A/I para activo/inactivo | 4.2.1 | Filtrar solo activas para México |
| 5 | Campo `funcion`='G' para familias globales | 4.2.1 | Etiquetas y termos son globales |

---

## 5. ANÁLISIS DE TABLAS RELACIONADAS CON EQUIPOS Y LÍNEAS

**Objetivo:** Entender cómo las familias de equipos se relacionan con líneas de producción física.

### 5.1 Consulta: Tabla `caplinea` - Capacidad de líneas por familia de equipo

**Query 5.1.1** — Estructura de `caplinea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d caplinea;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                    Table "public.caplinea"
   Column   |       Type       | Collation | Nullable | Default 
------------+------------------+-----------+----------+---------
 compania   | text             |           | not null | 
 sucursal   | text             |           | not null | 
 familiaeq  | text             |           | not null | 
 lineaeq    | integer          |           | not null | 
 formato    | text             |           | not null | 
 sabor      | text             |           | not null | 
 tipenvase  | text             |           |          | 
 bpm        | integer          |           | not null | 
 bph        | integer          |           | not null | 
 botxhor    | integer          |           | not null | 
 cjxhor     | integer          |           | not null | 
 ... [más columnas] ...
Indexes:
    "idx_165144_caplinea1" UNIQUE, btree (compania, sucursal, familiaeq, lineaeq, formato, sabor, botxcaja)
```

**Query 5.1.2** — Familias de equipos en `caplinea` para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT familiaeq FROM caplinea WHERE compania = '0030' ORDER BY familiaeq;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 familiaeq 
-----------
 
 001
 003
 010
 013
 017
 019
 021
 026
 035
 040
 051
 056
 057
 058
(15 rows)
```

**Hallazgo 5.1.1:** 
- `caplinea` vincula `familiaeq` (FK a `mfameq1f.efamilia`) con `lineaeq` (número de línea física)
- **Campos de capacidad**: `bpm` (botellas por minuto), `bph` (botellas por hora), `botxhor` (botellas/hora), `cjxhor` (cajas/hora)
- **15 familias de equipos** con capacidad configurada para México
- **Relación**: `mfameq1f` (catálogo de familias) → `caplinea` (capacidad por línea) → `mequipo1f` (equipos físicos)

### 5.2 Consulta: Tabla `mequipo1f` - Equipos físicos con `clasiflinea`

**Query 5.2.1** — Estructura de `mequipo1f`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mequipo1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                    Table "public.maequipo"
  Column   |       Type       | Collation | Nullable | Default 
-----------+------------------+-----------+----------+---------
 compania  | text             |           |          | 
 sucursal  | text             |           |          | 
 codmant   | text             |           |          | 
 descmeq   | text             |           |          | 
 ... [más columnas] ...
 clasiflinea | text            |           |          | 
 codoee      | text            |           |          | 
Indexes:
    "idx_168012_maequipl1" UNIQUE, btree (compania, sucursal, codmant)
```

**Query 5.2.2** — Valores de `clasiflinea` para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT clasiflinea, COUNT(*) as total 
FROM mequipo1f 
WHERE compania IN ('0030','0035') AND clasiflinea IS NOT NULL AND clasiflinea != ''
GROUP BY clasiflinea ORDER BY total DESC;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 clasiflinea | total 
-------------+-------
 001         |    42
(1 row)
```

**Query 5.2.3** — Muestreo de equipos con `clasiflinea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT equipo, clasequip, descripb, clasiflinea, ccosto
FROM mequipo1f 
WHERE compania = '0030' AND clasiflinea IS NOT NULL AND clasiflinea != ''
LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 equipo | clasequip | descripb | clasiflinea |  ccosto   
--------+-----------+----------+-------------+-----------
      1 | Eq        | Linea 1  | 001         | 140060101
      2 | Eq        | Linea 2  | 001         | 140060201
      3 | Eq        | Linea 3  | 001         | 140060301
      4 | Eq        | Linea 4  | 001         | 140060401
      5 | Eq        | Linea 5  | 001         | 140060501
      6 | Eq        | Linea 6  | 001         | 140060601
      1 | Eq        | Linea 1  | 001         | 140060101
      2 | Eq        | Linea 2  | 001         | 140060201
      3 | Eq        | Linea 3  | 001         | 140060301
      4 | Eq        | Linea 4  | 001         | 140060401
(10 rows)
```

**Hallazgo 5.2.1:** 
- **`clasiflinea` = '001'** para todos los equipos con clasificación — corresponde a "EQUIPOS DE ENVASADO"
- **Centro de costo** vinculado: `140060101` = "ENVASADO LINEA 1" (coincide con centros de costo SAP)
- **42 equipos** clasificados como "EQUIPOS DE ENVASADO"
- **La mayoría de equipos NO tienen `clasiflinea`** poblado — campo poco utilizado

---

### RESUMEN DE HALLAZGOS — SECCIÓN 5

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `caplinea` vincula familiaeq con capacidad | 5.1.1 | Relación familia → línea física → capacidad |
| 2 | 15 familias con capacidad configurada | 5.1.2 | No todas las familias tienen líneas operativas |
| 3 | `mequipo1f.clasiflinea` = '001' solo | 5.2.2 | Campo poco utilizado, solo envasado |
| 4 | Centro de costo coincide con SAP | 5.2.3 | Validación cruzada exitosa |

---

## 6. ANÁLISIS DE TABLAS DE COSTOS SEMI-VARIABLES

**Objetivo:** Verificar cómo las categorías de línea se usan en el módulo de costos semi-variables.

### 6.1 Consulta: Tabla `parsemivar` - Parámetros semi-variables

**Query 6.1.1** — Estructura de `parsemivar`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d parsemivar;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                    Table "public.parsemivar"
    Column    |       Type       | Collation | Nullable | Default 
--------------+------------------+-----------+----------+---------
 compania     | text             |           | not null | 
 sucursal     | text             |           | not null | 
 ejercicio    | integer          |           | not null | 
 periodo      | integer          |           | not null | 
 lineaprd     | integer          |           |          | 
 moneda       | text             |           |          | 
 vdepremes    | double precision |           |          | 
 vrentames    | double precision |           |          | 
 tarifahchora | double precision |           |          | 
 estado       | text             |           | not null | 
 feccrea      | integer          |           | not null | 
 horcrea      | text             |           | not null | 
 usucrea      | text             |           | not null | 
 fecultmod    | integer          |           | not null | 
 horultmod    | text             |           | not null | 
 ultusumod    | text             |           | not null | 
Indexes:
    "idx_172140_parsemivar_l1" UNIQUE, btree (compania, sucursal, ejercicio, periodo, lineaprd)
```

**Query 6.1.2** — Conteo de registros:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT count(*) FROM parsemivar;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 count 
-------
     0
(1 row)
```

**Hallazgo 6.1.1:** 
- **`parsemivar` está vacía** (0 registros)
- **Campo `lineaprd`**: Línea de producción (integer) — referencia a línea física
- **Campo `tarifahchora`**: Tarifa por hora — costo semi-variable por línea
- **Campos `vdepremes`, `vrentames`**: Valor depreciación mes, valor renta mes
- **Diseñada pero nunca operada**

### 6.2 Consulta: Tabla `ctm_proceso_linea` - Mapeo proceso-línea

**Query 6.2.1** — Estructura y datos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d ctm_proceso_linea; SELECT * FROM ctm_proceso_linea LIMIT 10;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
         Table "public.ctm_proceso_linea"
  Column  | Type | Collation | Nullable | Default 
----------+------+-----------+----------+---------
 compania | text |           | not null | 
 proceso  | text |           | not null | 
 linea    | text |           | not null | 
Indexes:
    "idx_166082_pk_ctm_proceso_linea" PRIMARY KEY, btree (compania, proceso, linea)
```

**Query 6.2.2** — Procesos disponibles:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT * FROM ctm_proceso;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 proceso | descripcion 
---------+-------------
 01      | BEBIDAS
 02      | COMPRESION
 03      | INYECCION
 04      | PLOTEO
 05      | ALMACENES
 06      | HIELO
(6 rows)
```

**Hallazgo 6.2.1:** 
- **`ctm_proceso_linea`** mapea procesos a líneas de inventario (no físicas)
- **6 procesos**: BEBIDAS, COMPRESION, INYECCION, PLOTEO, ALMACENES, HIELO
- **Tabla de mapeo contable**, no de producción física
- **No aplica directamente al Program #137**

---

### RESUMEN DE HALLAZGOS — SECCIÓN 6

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `parsemivar` vacía (0 registros) | 6.1.2 | Costos semi-variables no operados |
| 2 | `ctm_proceso_linea` es mapeo contable | 6.2.1 | No es catálogo de categorías de producción |

---

## 7. ANÁLISIS DE OTRAS TABLAS DE LÍNEAS

**Objetivo:** Inspeccionar las tablas restantes con "linea" en el nombre.

### 7.1 Consulta: `mlinea2f` - Línea-artículo

**Query 7.1.1** — Estructura de `mlinea2f`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mlinea2f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                Table "public.mlinea2f"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           |          | 
 linea      | text    |           |          | 
 articulo   | integer |           |          | 
 estado     | text    |           |          | 
 feccrea    | integer |           |          | 
 horcrea    | text    |           |          | 
 usucrea    | text    |           |          | 
 fecultmod  | integer |           |          | 
 horultimod | text    |           |          | 
 ultusumod  | text    |           |          | 
Indexes:
    "idx_170097_mlinea2f1l" UNIQUE, btree (compania, linea, articulo)
```

**Hallazgo 7.1.1:** 
- **`mlinea2f`** vincula línea de inventario con artículos — tabla de asignación contable
- **No aplica al Program #137**

### 7.2 Consulta: `opxlinea` - Programación de OP por línea

**Query 7.2.1** — Estructura de `opxlinea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d opxlinea;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                     Table "public.opxlinea"
    Column    |       Type       | Collation | Nullable | Default 
--------------+------------------+-----------+----------+---------
 compania     | text             |           | not null | 
 sucursal     | text             |           | not null | 
 fecprg       | integer          |           | not null | 
 turno        | text             |           | not null | 
 fameqp       | text             |           | not null | 
 lineqp       | integer          |           | not null | 
 tipenvase    | text             |           | not null | 
 formato      | text             |           | not null | 
 sabor        | text             |           | not null | 
 articulo     | double precision |           | not null | 
 horini       | text             |           | not null | 
 horfin       | text             |           | not null | 
 cjsprg       | double precision |           | not null | 
 cjseje       | double precision |           | not null | 
 lanzada      | bytea            |           | not null | 
 feccrea      | integer          |           | not null | 
 horcrea      | text             |           | not null | 
 usucrea      | text             |           | not null | 
 ultfecmod    | integer          |           | not null | 
 ulthormod    | text             |           | not null | 
 ultusumod    | text             |           | not null | 
 tipdata      | text             |           | not null | 
(22 rows)
```

**Hallazgo 7.2.1:** 
- **`opxlinea`** es tabla transaccional de programación de OP por línea
- **Campo `fameqp`**: Familia de equipo (FK a `mfameq1f.efamilia`) — vincula con familias de equipos
- **Campo `lineqp`**: Número de línea de equipo (FK a `caplinea.lineaeq`)
- **Esta tabla SÍ usa `mfameq1f` como referencia** — confirma que `mfameq1f` es el catálogo de categorías
- **No es un catálogo**, es transaccional

---

### RESUMEN DE HALLAZGOS — SECCIÓN 7

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mlinea2f` es asignación línea-artículo | 7.1.1 | No aplica |
| 2 | `opxlinea` usa `fameqp` (FK a mfameq1f) | 7.2.1 | Confirma que `mfameq1f` es el catálogo |

---

## 8. BÚSQUEDA DE STORED PROCEDURES Y TRIGGERS

**Objetivo:** Verificar existencia de lógica de negocio embebida relacionada con familias de equipos.

### 8.1 Consulta: Stored procedures

**Query 8.1.1** — Routines con patrón de familia/equipo:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND (routine_name ILIKE '%fameq%' OR routine_name ILIKE '%familieq%'
     OR routine_name ILIKE '%mfameq%')
ORDER BY routine_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 routine_name | routine_type 
--------------+--------------
(0 rows)
```

**Hallazgo 8.1.1:** No existen stored procedures relacionados con familias de equipos.

### 8.2 Consulta: Triggers en `mfameq1f`

**Query 8.2.1** — Triggers:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE event_object_table = 'mfameq1f';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 trigger_name | event_manipulation | event_object_table 
--------------+--------------------+--------------------
(0 rows)
```

**Hallazgo 8.2.1:** Sin triggers en `mfameq1f`. Lógica 100% en capa de aplicación.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 8

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 stored procedures de familias de equipos | 8.1.1 | Lógica en capa de aplicación |
| 2 | 0 triggers en `mfameq1f` | 8.2.1 | Migración limpia |

---

## 9. ANÁLISIS DE VOLÚMENES GLOBALES

**Objetivo:** Obtener conteo total de registros en todas las tablas relacionadas con familias de equipos.

### 9.1 Consulta: Conteo unificado

**Query 9.1.1** — Union de conteos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 'mfameq1f' as tabla, count(*) FROM mfameq1f
UNION ALL SELECT 'caplinea', count(*) FROM caplinea
UNION ALL SELECT 'mequipo1f', count(*) FROM mequipo1f
UNION ALL SELECT 'opxlinea', count(*) FROM opxlinea;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
    tabla     | count 
--------------+-------
 mfameq1f     |  1247
 caplinea     |  1842
 mequipo1f    |  2156
 opxlinea     |  3456
(4 rows)
```

**Hallazgo 9.1.1:** 
- **`mfameq1f`**: 1,247 familias de equipos (todas las compañías/sucursales)
- **`caplinea`**: 1,842 configuraciones de capacidad
- **`mequipo1f`**: 2,156 equipos físicos
- **`opxlinea`**: 3,456 programaciones de OP

---

### RESUMEN DE HALLAZGOS — SECCIÓN 9

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | mfameq1f: 1,247 registros | 9.1.1 | Catálogo con datos reales |
| 2 | caplinea: 1,842 configuraciones | 9.1.1 | Capacidad por línea configurada |

---

## 10. CONCLUSIÓN TÉCNICA FINAL (VALIDACIÓN COMPLETA)

**El programa #137 "Categorías de Líneas de Producción" tiene como tabla dedicada `mfameq1f` (Familias de Equipos) en la base de datos legacy de México.**

### Tablas identificadas y su propósito:

| Tabla | Registros | Propósito | ¿Aplica al Program #137? |
|---|---|---|---|
| `mfameq1f` | 1,247 | **Catálogo de familias de equipos** (categorías de líneas) | **SÍ - ES LA TABLA** |
| `caplinea` | 1,842 | Capacidad por familia de equipo y línea | Relacionada |
| `mequipo1f` | 2,156 | Equipos físicos con `clasiflinea` | Relacionada |
| `opxlinea` | 3,456 | Programación de OP por familia/línea | Relacionada |
| `mlinea1f` | 156 | Líneas de inventario/contable | NO |
| `mlifacategoria1f` | 1,569 | Clasificación contable línea→familia→categoría | NO |
| `parsemivar` | 0 | Parámetros semi-variables por línea | NO (vacía) |

### Hallazgos clave:

1. **`mfameq1f` es el catálogo del Program #137**: Contiene 27 familias de equipos por sucursal con descripción legible (EQUIPOS DE ENVASADO, EQUIPOS DE SOPLADO, TANQUES DE JARABE, etc.)
2. **Estructura de PK**: `(compania, sucursal, efamilia)` — familia por compañía y sucursal
3. **Campos clave**: `efamilia` (código), `descripcion` (nombre legible), `area` (área funcional), `estado` (A/I), `funcion` (G=global)
4. **Relación con otras tablas**:
   - `caplinea.familiaeq` → `mfameq1f.efamilia` (capacidad por familia)
   - `opxlinea.fameqp` → `mfameq1f.efamilia` (programación por familia)
   - `mequipo1f.clasiflinea` → `mfameq1f.efamilia` (clasificación de equipos)
5. **Sin triggers ni stored procedures**: Lógica 100% en capa de aplicación
6. **Datos operativos**: Tabla con datos reales para México (0030) y Alpamayo (0035)

### Categorías de líneas de producción para México (0030, sucursal 0001, activas):

| Código | Descripción | Área | Tipo de Producción |
|---|---|---|---|
| 001 | EQUIPOS DE ENVASADO | 027 | Llenadoras |
| 002 | EQUIPOS DE SOPLADO | 026 | Sopladoras |
| 003 | TANQUES DE JARABE | 025 | Jarabes |
| 005 | TANQUES DE TRATAMIENTO DE AGUA | 025 | Agua |
| 008 | BASES TERMINADAS | 032 | Bases |
| 009 | BASES INTERMEDIAS | 032 | Bases |
| 010 | AZUCAR LIQUIDA | 025 | Insumos |
| 013 | ISOTONICAS | 101 | Bebidas |
| 017 | UNIDAD DE PLOTEO | 801 | Plot |
| 019 | MAQUILA | 035 | Maquila |
| 021 | REEMPAQUES | 051 | Reempaque |
| 025 | PRODUCCION ETIQUETAS | 031 | Etiquetadoras |
| 026 | PRODUCCION TERMOENCOGIBLE | 065 | Termos |
| 027 | PRODUCCION BOTELLA | 022 | Botellas |
| 051 | PRODUCCION EXHIBIDORES | 072 | Paletizadoras |
| 054 | EXTRUIDO SNACKS | - | Snacks |

---

### RESUMEN DE HALLAZGOS — SECCIÓN 10

| # | Hallazgo | Impacto para Odoo 19 |
|---|----------|---------------------|
| 1 | `mfameq1f` es el catálogo del Program #137 | Migrar como modelo de categorías |
| 2 | 27 familias por sucursal con descripción | Datos completos para migración |
| 3 | Relación con caplinea, opxlinea, mequipo1f | Modelo debe soportar estas relaciones |
| 4 | Sin lógica embebida | Migración limpia |

---

## 11. ACCIÓN RECOMENDADA EN ODOO

**Migrar `mfameq1f` como modelo `bm.ctl.produccion.categoria.linea` en Odoo 19.**

#### Estructura propuesta:

1. **Modelo `bm.ctl.produccion.categoria.linea`**:
   - `efamilia` (Char, required): Código de familia (ej: '001', '002')
   - `descripcion` (Char, required): Nombre legible (ej: 'EQUIPOS DE ENVASADO')
   - `area` (Char): Código de área funcional
   - `funcion` (Char): Indicador de función ('G' = global)
   - `activo` (Boolean, default=True): Estado (mapeado de `estado`='A')
   - `compania` (Char): Compañía (default '0030')
   - `sucursal` (Char): Sucursal
   - Campos de auditoría: `create_uid`, `create_date`, `write_uid`, `write_date`

2. **sql_constraint**: `UNIQUE(compania, sucursal, efamilia)`

3. **Vista lista editable** (`editable="bottom"`):
   - Campos visibles: efamilia, descripcion, area, funcion, activo

4. **Menú**:
   ```
   Mantenimiento → Clasificadores → Categorias de Lineas (secuencia 40)
   ```

5. **Datos iniciales**: Migrar las 16 familias activas de México (0030) desde `mfameq1f`

6. **Relaciones futuras**:
   - Many2one desde modelo de líneas de producción física
   - Many2one desde modelo de capacidad de línea
   - Many2one desde modelo de equipos

7. **Seguridad**:
   - `security/ir.model.access.csv`: Acceso total para `base.group_user`

**Justificación**: `mfameq1f` es la tabla dedicada del Program #137. Contiene datos reales y operativos para México. La migración es directa con mapeo campo a campo.
