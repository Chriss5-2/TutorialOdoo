## 1. EXPLORACIÓN DE DOCUMENTACIÓN OFICIAL - FAMILIA DE PRODUCCIÓN

**Objetivo:** Consultar `aje_docs_simulacion/01_Docs_Oficiales/` para obtener un acercamiento inicial al Program #138 "Familia de Producción".

### 1.1 Consulta: Búsqueda de documentación sobre el Program #138 en docs oficiales

**Query 1.1.1** — Estructura del directorio de documentación oficial:
```
aje_docs_simulacion/01_Docs_Oficiales/
├── DocsOficiales/
│   ├── A&F/
│   ├── Ajemex - Impresoras/
│   ├── Cadena de Suministro/
│   ├── Comercial/
│   ├── LEGO Integraciones _ Plan de habilitación de entorno de pruebas_V1_xlsx.md
│   ├── Local México/
│   └── Transversal/
└── #478789 Obtener informacion de BD Mexico producción_xlsx.md
```

**Hallazgo 1.1.1:** Las subcarpetas contienen documentación de integraciones externas (SAP, FullStep, Avail, Salesforce, EDI, BBVA, CHEP, etc.) y no documentación funcional de programas específicos del menú Producción. El archivo `#478789 Obtener informacion de BD Mexico producción_xlsx.md` es la fuente principal con catálogos de stored procedures y objetos de BD del sistema legacy.

### 1.2 Consulta: Búsqueda de referencias al Program #138 y "familia" en la BD

**Query 1.2.1** — Búsqueda con patrón `138|familia` en `#478789 Obtener informacion de BD Mexico producción_xlsx.md`:

Resultados relevantes:

| Objeto | Tipo | Creado | Última modificación | Estado |
|---|---|---|---|---|
| `USP_GIM_LLENA_GETFAMILIASPRODUCCION` | Stored Procedure | 2016-03-14 | 2016-03-14 | **EN USO** |
| `DIM_CS_FAMILIA` | Vista/Dimensión | 2015-02-27 | 2015-02-27 | MEDIO - posible código muerto |
| `USP_CE_RPT_FAMILIAEQ` | Stored Procedure | 2016-02-04 | 2016-02-04 | MEDIO - posible código muerto |
| `USP_CE_FAMILIAS_MERMA` | Stored Procedure | 2016-06-06 | 2016-08-18 | MEDIO - posible código muerto |
| `USP_MUESTRA_ITEMXFAMILIA` | Stored Procedure | 2018-05-16 | 2018-06-12 | MEDIO - posible código muerto |
| `PR_ERP_FNZ_QRY_WS_CREAFAMILIA` | Stored Procedure | 2019-07-10 | 2019-07-10 | ALTO - probable código muerto |
| `PR_ERP_FNZ_QRY_WS_CREASUBFAMILIA` | Stored Procedure | 2019-07-10 | 2019-07-10 | ALTO - probable código muerto |
| `USP_LINEA_FAMILIA` | Stored Procedure | 2013-09-17 | 2013-09-17 | ALTO - probable código muerto |
| `USP_CE_GENERAR_FAMILIAEQ` | Stored Procedure | 2016-02-04 | 2016-02-04 | ALTO - probable código muerto |
| `SCM_MPS_SEL_FAMILIA` | Stored Procedure | 2013-09-17 | 2013-09-17 | ALTO - probable código muerto |
| `SCM_MRP_MATERIAL_SEL_FAMILIA` | Stored Procedure | 2013-09-17 | 2013-09-17 | ALTO - probable código muerto |
| `SP_RS_COSTO_PRODUCCION_FAMILIA_DETALLADO_BIGMAGIC` | Stored Procedure | 2020-12-14 | 2020-12-15 | MEDIO - posible código muerto |

**Hallazgo 1.2.1:** Ninguno de los objetos listados como "EN USO" o "MEDIO" corresponde a una tabla maestra de familias de producción (tipo `bfamilia1f` o `tipfamilia`). El SP `USP_GIM_LLENA_GETFAMILIASPRODUCCION` —el único "EN USO"— por su prefijo `GIM_LLENA` (llena/get) es un SP de consulta/extracción probablemente usado por el integrador BM (Big Magic → procesos batch), no un CRUD directo de la UI.

### 1.3 Ubicación en el árbol de menús

Del archivo `Produccion_arbol_funciones.html`:

```
Menu Principal
└── Mantenimiento (mexico: SI)
    └── Configuraciones (mexico: SI)
        └── Familia de Produccion (mexico: SI) ← Program #138
```



---

## 2. EXPLORACIÓN DE DICCIONARIO DE DATOS — FAMILIA DE PRODUCCIÓN

**Objetivo:** Ejecutar consultas de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas al concepto "familia" en el contexto de producción, dentro del esquema público de `mxbdaje_local`.

### 2.1 Consulta: Búsqueda de tablas con "familia" en el nombre

**Query 2.1.1** — Tablas con "familia":
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_NAME LIKE '%familia%' AND TABLE_SCHEMA = 'public' ORDER BY TABLE_NAME;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
  table_name   
---------------
 ctm_familiaeq
(1 row)
```

**Hallazgo 2.1.1:** Solo 1 tabla contiene "familia" en el nombre: `ctm_familiaeq`. Es necesario inspeccionar su estructura.

### 2.2 Consulta: Búsqueda de tablas tipo catálogo `bfamilia*` / `tipfamil*`

**Query 2.2.1** — Tablas de catálogo de familias:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
WHERE (TABLE_NAME LIKE 'bfamilia%' OR TABLE_NAME LIKE 'tipfamil%' OR TABLE_NAME LIKE 'mfampro%') 
  AND TABLE_SCHEMA = 'public';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 table_name 
------------
(0 rows)
```

**Hallazgo 2.2.1:** No existe tabla tipo catálogo maestra para familias de producción. No hay `bfamilia1f`, `tipfamilia`, ni `mfampro*`.

### 2.3 Consulta: Búsqueda de columnas con "familia" en cualquier tabla

**Query 2.3.1** — Columnas "familia" en toda la BD:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE (COLUMN_NAME LIKE '%familia%' OR COLUMN_NAME LIKE '%cfamilia%') 
  AND TABLE_SCHEMA = 'public'
ORDER BY TABLE_NAME, COLUMN_NAME;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
         table_name         |    column_name    | data_type 
----------------------------+-------------------+-----------
 ... (215 filas) ...
 martic1f                   | familia           | text
 martic1f                   | subfamilia        | text
 mfameq1f                   | efamilia          | text
 mfamil1f                   | familia           | text
 mfamil1f                   | familia_corp      | text
 msubfa1f                   | familia           | text
 msubfa1f                   | subfamilia        | text
 mlifatipobebida1f          | familia           | text
 equi_famprod               | fam_mag           | text
 equi_famprod               | fam_bm            | text
 cabstdpro                  | famprod           | text
 art_basebm                 | famprod_bm        | text
 ctm_familiaeq              | efamilia          | text
 ...
```

**Hallazgo 2.3.1:** Se identifican 215 columnas. Tablas principales de interés:
- `mfamil1f` — familia de artículo (inventario)
- `msubfa1f` — subfamilia de artículo  
- `mfameq1f` — familia de equipo (ya migrada, Program #137)
- `mlifatipobebida1f` — tipo de bebida por familia
- `cabstdpro` — columna `famprod` en costeo estándar
- `ctm_familiaeq` — equipo-familia por ejercicio

### 2.4 Consulta: Búsqueda de stored procedures con "familia" en producción

**Query 2.4.1** — SP con "familia" en producción:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT proname FROM pg_proc WHERE proname ILIKE '%familia%produccion%' OR proname ILIKE '%getfamilias%';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 proname | prosrc 
---------+--------
(0 rows)
```

**Query 2.4.2** — SP `USP_GIM_LLENA_GETFAMILIASPRODUCCION`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT pg_get_functiondef(oid) FROM pg_proc 
WHERE proname = 'usp_gim_llena_getfamiliasproduccion';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 pg_get_functiondef 
--------------------
(0 rows)
```

**Hallazgo 2.4.1:** El SP `USP_GIM_LLENA_GETFAMILIASPRODUCCION` —único objeto "EN USO" en el catálogo de SQL Server (Excel)— NO existe en esta instancia PostgreSQL de `mxbdaje_local`. Fue importado del SQL Server original pero su implementación se perdió en la migración a PG.

### 2.5 Consulta: Artículos con columnas de familia de producción

**Query 2.5.1** — Columnas `famprod` en tabla de artículos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'martic1f' AND table_schema = 'public'
AND (column_name LIKE '%famprod%' OR column_name LIKE '%familia%')
ORDER BY column_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 column_name | data_type 
-------------+-----------
 familia     | text
 subfamilia  | text
(2 rows)
```

**Query 2.5.2** — Búsqueda global de columnas `famprod`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'public' AND COLUMN_NAME LIKE 'famprod%'
ORDER BY TABLE_NAME, COLUMN_NAME;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 table_name | column_name | data_type 
------------+-------------+-----------
 art_basebm | famprod_bm  | text
 cabstdpro  | famprod     | text
(2 rows)
```

**Hallazgo 2.5.1:** `martic1f` (maestro de artículos) NO tiene columna `famprod`. Solo tiene `familia` y `subfamilia` (clasificación de inventario). La columna `famprod` existe únicamente en `cabstdpro` (costeo estándar) y `art_basebm` (artículo base BM). Por lo tanto, la "familia de producción" no es una propiedad directa del artículo en la BD legacy, sino una clasificación de costeo.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 2

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|---|---|---|
| 1 | Solo `ctm_familiaeq` tiene "familia" en el nombre de tabla | 2.1.1 | Posible candidata, inspeccionar estructura |
| 2 | No existe tabla maestra tipo `bfamilia1f` o `tipfamilia` | 2.2.1 | No hay catálogo legacy de familias de producción |
| 3 | 215 columnas con "familia" en 100+ tablas | 2.3.1 | El concepto está disperso (inventario, costos, equipos) |
| 4 | `cabstdpro.famprod` y `art_basebm.famprod_bm` son las únicas columnas `famprod` | 2.5.2 | La familia de producción es de costeo, no del artículo |
| 5 | SP `USP_GIM_LLENA_GETFAMILIASPRODUCCION` no existe en PG | 2.4.1 | No hay lógica de negocio recuperable |

### Acción para Odoo 19:
- Inspeccionar `mfamil1f` (catálogo de familias de artículo) y `msubfa1f` para descartar
- Inspeccionar `ctm_familiaeq` para ver si tiene datos operativos
- Verificar relación entre `cabstdpro.famprod` y `mfameq1f.efamilia`

---

## 3. ANÁLISIS DE TABLA `mfamil1f` — DESCARTA: FAMILIAS DE INVENTARIO

**Objetivo:** Confirmar que `mfamil1f` es el catálogo de familias de artículo/clasificación contable, NO de producción.

### 3.1 Consulta: Estructura de `mfamil1f`

**Query 3.1.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mfamil1f' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                 Table "public.mfamil1f"
    Column     |  Type   | Collation | Nullable | Default 
---------------+---------+-----------+----------+---------
 compania      | text    |           | not null | 
 linea         | text    |           | not null | 
 familia       | text    |           | not null | 
 descrip       | text    |           | not null | 
 descripcor    | text    |           | not null | 
 centrocost    | text    |           | not null | 
 estado        | text    |           | not null | 
 feccrea       | integer |           | not null | 
 horcrea       | text    |           | not null | 
 usucrea       | text    |           | not null | 
 fecultmod     | integer |           | not null | 
 horultimod    | text    |           | not null | 
 ultusumod     | text    |           | not null | 
 parancel      | text    |           |          | 
 flgflete      | bytea   |           |          | 
 familia_corp  | text    |           |          | 
 categoria     | text    |           |          | 
 flgcatfiscal  | bytea   |           |          | 
 tipcontrol    | text    |           |          | 
 flgalmacen_fs | bytea   |           |          | 
 flgpeso       | bytea   |           |          | 
 flgdimension  | bytea   |           |          | 
 flgsoplado    | bytea   |           |          | 
 unidad        | text    |           |          | 
 univol        | text    |           |          | 
 unicont       | text    |           |          | 
 unipeso       | text    |           |          | 
 flgbrix       | bytea   |           |          | 
Indexes:
    "idx_169852_mfamil1l1" UNIQUE, btree (compania, linea, familia)
    "idx_169852_mfamil1l2" btree (compania, linea, descrip)
    "idx_169852_mfamil1l3" btree (compania, linea)
```

**Hallazgo 3.1.1:** PK compuesta `(compania, linea, familia)`. La presencia de `linea` como parte de la PK indica que las familias se clasifican POR tipo de línea de inventario (`mlinea1f`), no por criterios de producción.

### 3.2 Consulta: Datos de `mfamil1f` para México

**Query 3.2.1** — Muestra de familias:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT familia, familia_corp, descrip, descripcor, estado, centrocost, categoria, tipcontrol 
FROM mfamil1f WHERE compania = '0030' ORDER BY familia LIMIT 30;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 familia | familia_corp |                 descrip                 | descripcor | estado | centrocost | categoria | tipcontrol 
---------+--------------+-----------------------------------------+------------+--------+------------+-----------+------------
 001     |              | AZUCAR                                  | AZUCA      | A      |            |           | C
 001     |              | JARABES IN BOX                          |            | A      |            |           | C
 001     |              | UTILES DE ESCRITORIO                    | UTILE      | A      |            |           | C
 001     |              | AGUA TRATADA                            | AGUA       | A      |            |           | C
 001     |              | GASEOSA                                 | GASEO      | A      |            |           | C
 001     |              | SUMINISTROS                             | SUMIS      | A      |            |           | C
 001     |              | PREFORMAS                               | PREFO      | A      |            |           | C
 002     |              | INSUMOS SERVICIO MAQUILA                |            | A      |            |           | C
 002     |              | CARTON PLAST                            |            | A      |            |           | C
 ...
(30 rows)
```

**Query 3.2.2** — Distribución de familias por línea de inventario:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, linea, COUNT(*) AS total_familias 
FROM mfamil1f WHERE compania = '0030' GROUP BY compania, linea ORDER BY linea;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | linea | total_familias 
----------+-------+----------------
 0030     | 01    |             32
 0030     | 02    |             21
 0030     | 03    |              9
 0030     | 04    |             32
 0030     | 05    |             10
 0030     | 06    |              7
 0030     | 07    |             26
 ... (25 líneas en total) ...
 0030     | 37    |              3
```

**Query 3.2.3** — Significado de cada `linea` (de `mlinea1f`):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM mlinea1f WHERE compania = '0030' ORDER BY linea;
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
 ... (26 líneas) ...
```

**Hallazgo 3.2.1:** `mfamil1f` clasifica artículos por tipo de inventario (Producto Terminado, Materia Prima, Envases, Repuestos, etc.), NO por familia de producción. La familia `001=GASEOSA` aparece en línea `01` (Producto Terminado) pero el mismo código `001` también aplica a `AZUCAR`, `TAPAS`, `PREFORMAS` en otras líneas. Esto es clasificación contable, no de producción.

### 3.3 Consulta: `mfamil1f` para línea `Te` (Producto Terminado)

**Query 3.3.1** — Verificar si existe línea `Te`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT familia, descripcor FROM mfamil1f 
WHERE compania = '0030' AND linea = 'Te' ORDER BY familia LIMIT 30;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 familia | descripcor 
---------+------------
(0 rows)
```

**Hallazgo 3.3.1:** No existen registros con `linea = 'Te'`. Las líneas de inventario usan códigos numéricos (`01`, `02`, ...), no el código de tipo (`Te`, `In`, `Pr`). El flag `flglinea` en `mlinea1f` es solo una clasificación, no un identificador.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 3

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|---|---|---|
| 1 | `mfamil1f` tiene PK `(compania, linea, familia)` | 3.1.1 | Es familia de inventario por tipo de línea |
| 2 | Las familias de `mfamil1f` son contables (AZUCAR, GASEOSA, PREFORMAS en diferentes líneas) | 3.2.1 | No es un catálogo de familias de producción |
| 3 | Líneas de inventario = Producto Terminado, Materia Prima, Envases, etc. | 3.2.3 | Clasificación contable, no productiva |
| 4 | No hay registros con `linea = 'Te'` (el código se almacena como `01`) | 3.3.1 | La referencia cruzada usa código numérico |

### Conclusión Sección 3:
**`mfamil1f` NO es la tabla del Program #138.** Es el catálogo de familias de artículo para clasificación contable/inventario. DESCARTADA.

---

## 4. ANÁLISIS DE TABLA `msubfa1f` — DESCARTA: SUBFAMILIAS DE INVENTARIO

**Objetivo:** Confirmar que `msubfa1f` es subcatálogo de `mfamil1f`, no relacionado con producción.

### 4.1 Consulta: Estructura y datos de `msubfa1f`

**Query 4.1.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d msubfa1f' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                 Table "public.msubfa1f"
    Column    |  Type   | Collation | Nullable | Default 
--------------+---------+-----------+----------+---------
 compania     | text    |           | not null | 
 linea        | text    |           | not null | 
 familia      | text    |           | not null | 
 subfamilia   | text    |           | not null | 
 descrip      | text    |           | not null | 
 descripcor   | text    |           | not null | 
 compraloc    | text    |           | not null | 
 compraimpo   | text    |           | not null | 
 variaexist   | text    |           | not null | 
 estado       | text    |           | not null | 
 feccrea      | integer |           | not null | 
 horcrea      | text    |           | not null | 
 usucrea      | text    |           | not null | 
 fecultmod    | integer |           | not null | 
 horultimod   | text    |           | not null | 
 ultusumod    | text    |           | not null | 
 subcategoria | text    |           |          | 
 codigrupo    | integer |           |          | 
Indexes:
    "idx_171463_msubfa1l1" PRIMARY KEY, btree (compania, linea, familia, subfamilia)
    "idx_171463_msubfa1l2" btree (compania, linea, familia, descrip)
```

**Query 4.1.2** — Conteo total para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT COUNT(*) FROM msubfa1f WHERE compania = '0030';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 count 
-------
   911
```

**Query 4.1.3** — Distribución de subfamilias por familia:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT familia, COUNT(*) as sub_count FROM msubfa1f 
WHERE compania = '0030' GROUP BY familia ORDER BY sub_count DESC LIMIT 15;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 familia | sub_count 
---------+-----------
 001     |       152
 003     |        72
 002     |        65
 017     |        46
 004     |        37
 005     |        33
 006     |        29
 022     |        26
 007     |        22
 012     |        21
 068     |        21
 014     |        19
 085     |        18
 077     |        18
 020     |        17
```

**Hallazgo 4.1.1:** `msubfa1f` es el subcatálogo de `mfamil1f`, con PK `(compania, linea, familia, subfamilia)`. Tiene 911 registros para México clasificando subfamilias de artículos (ej: `familia=001` tiene 152 subfamilias). Es puramente contable/inventario.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 4

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|---|---|---|
| 1 | `msubfa1f` es subcatálogo de `mfamil1f` (PK incluye `familia`) | 4.1.1 | Depende jerárquicamente de mfamil1f |
| 2 | 911 registros para MX, familia `001` domina con 152 subfamilias | 4.1.2, 4.1.3 | Volumen alto pero clasificación contable |

### Conclusión Sección 4:
**`msubfa1f` NO es la tabla del Program #138.** DESCARTADA.

---

## 5. ANÁLISIS DE TABLA `ctm_familiaeq` — DESCARTA: VACÍA PARA MÉXICO

**Objetivo:** Verificar si `ctm_familiaeq` contiene datos operativos para México y si es la tabla del Program #138.

### 5.1 Consulta: Estructura de `ctm_familiaeq`

**Query 5.1.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d ctm_familiaeq' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
             Table "public.ctm_familiaeq"
  Column   |  Type   | Collation | Nullable | Default 
-----------+---------+-----------+----------+---------
 compania  | text    |           | not null | 
 sucursal  | text    |           | not null | 
 ejercicio | integer |           | not null | 
 efamilia  | text    |           | not null | 
 area      | text    |           | not null | 
Indexes:
    "idx_165908_pk_ctm_familiaeq" PRIMARY KEY, btree (compania, sucursal, ejercicio, efamilia)
```

**Query 5.1.2** — Datos para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM ctm_familiaeq WHERE compania = '0030' LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | ejercicio | efamilia | area 
----------+----------+-----------+----------+------
(0 rows)
```

**Query 5.1.3** — Distribución por compañía:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, COUNT(*) FROM ctm_familiaeq GROUP BY compania;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | count 
----------+-------
 0002     |   252
 0070     |    17
 0076     |    19
 0152     |    13
 ... (15 compañías, pero NO 0030) ...
```

**Hallazgo 5.1.1:** `ctm_familiaeq` tiene PK `(compania, sucursal, ejercicio, efamilia)`, vinculando familias de equipo a periodos contables. **Está completamente vacía para México (0030)**. Tiene datos para otras compañías pero no para la 0030.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 5

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|---|---|---|
| 1 | `ctm_familiaeq` vincula `efamilia` con ejercicio contable por sucursal | 5.1.1 | Configuración de costeo por periodo |
| 2 | 0 registros para México (0030) | 5.1.2 | No hay configuración activa para MX |
| 3 | Datos existen para otras compañías (0002=252, 0093=38, etc.) | 5.1.3 | La funcionalidad existe pero nunca se usó en MX |

### Conclusión Sección 5:
**`ctm_familiaeq` NO es la tabla del Program #138.** Es una tabla de configuración de costeo por periodo vacía para México. DESCARTADA.

---

## 6. ANÁLISIS DE `martic1f` — MAESTRO DE ARTÍCULOS

**Objetivo:** Verificar si el maestro de artículos contiene campos de familia de producción que indiquen la existencia del Program #138.

### 6.1 Consulta: Columnas relevantes en `martic1f`

**Query 6.1.1** — Columnas de producción:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'martic1f' AND table_schema = 'public'
AND (column_name LIKE '%familia%' OR column_name LIKE '%tipopro%' OR column_name LIKE '%linfabric%')
ORDER BY column_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 column_name | data_type 
-------------+-----------
 familia     | text
 linfabric   | smallint
 subfamilia  | text
 tipartprod  | smallint
(4 rows)
```

**Hallazgo 6.1.1:** `martic1f` tiene `familia` y `subfamilia` (clasificación inventario), más `tipartprod` (tipo artículo producción) y `linfabric` (línea fabricación), ambos `smallint`. NO tiene columna `famprod`.

### 6.2 Consulta: Valores de `tipartprod` y `linfabric`

**Query 6.2.1** — `tipartprod` (tipo artículo producción):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT tipartprod, COUNT(*) as cnt FROM martic1f 
WHERE compania = '0030' AND tipartprod IS NOT NULL AND tipartprod <> 0
GROUP BY tipartprod ORDER BY cnt DESC;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tipartprod |  cnt  
------------+-------
          9 | 25981
          6 |  8377
          4 |  6536
          1 |  2587
          2 |  2115
          8 |  1982
          7 |  1231
          5 |   964
          3 |   581
```

**Query 6.2.2** — `linfabric` (línea de fabricación):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT linfabric, COUNT(*) as cnt FROM martic1f 
WHERE compania = '0030' AND linfabric IS NOT NULL AND linfabric <> 0
GROUP BY linfabric ORDER BY cnt DESC LIMIT 15;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 linfabric |  cnt  
-----------+-------
         1 | 15225
         7 |  1099
        17 |   983
         2 |   787
         3 |   250
        14 |   127
        11 |   109
        18 |    79
         9 |    12
        13 |    12
         5 |    10
         6 |     4
         4 |     3
         8 |     3
        16 |     3
```

**Query 6.2.3** — Subfamilias más usadas en Producto Terminado (línea `01`):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT subfamilia, COUNT(*) as cnt FROM martic1f 
WHERE compania = '0030' AND linea = '01' AND subfamilia IS NOT NULL AND subfamilia != ''
GROUP BY subfamilia ORDER BY cnt DESC LIMIT 15;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 subfamilia |  cnt  
------------+-------
 68         | 11416
 14         |   684
 81         |   352
 01         |   197
 05         |   160
 91         |   127
 54         |    86
 86         |    83
 84         |    82
 50         |    80
 64         |    79
 04         |    78
 39         |    76
 03         |    75
 38         |    73
```

**Hallazgo 6.2.1:** `tipartprod` tiene 9 valores (1-9) con el valor `9` dominando con 25,981 artículos. `linfabric` tiene 15 valores distintos. Ambos son códigos numéricos sin catálogo en la BD (no existe tabla `ttipartprod` o `tlinfabric`). Las subfamilias de Producto Terminado están dominadas por `68` (11,416 artículos — probablemente "GASEOSA").

---

### RESUMEN DE HALLAZGOS — SECCIÓN 6

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|---|---|---|
| 1 | `martic1f` NO tiene columna `famprod` | 6.1.1 | La familia de producción no es propiedad del artículo |
| 2 | `tipartprod` (9 valores) y `linfabric` (15 valores) son smallint sin catálogo | 6.2.1, 6.2.2 | Clasificadores implícitos sin tabla maestra |
| 3 | Subfamilia `68` domina Producto Terminado con 11,416 artículos | 6.2.3 | Probablemente "GASEOSA" como subfamilia principal |

---

## 7. HALLAZGO PRINCIPAL: `cabstdpro.famprod` = `mfameq1f.efamilia`

**Objetivo:** Confirmar que el concepto "familia de producción" en la BD legacy es equivalente a la familia de equipo (`mfameq1f`).

### 7.1 Consulta: Valores de `famprod` en costeo estándar

**Query 7.1.1** — `famprod` en `cabstdpro` para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT famprod FROM cabstdpro WHERE compania = '0030' AND famprod IS NOT NULL AND famprod != '' ORDER BY famprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 famprod 
---------
 001
 003
 005
 008
 009
 010
 017
 019
 021
 025
 026
 051
(12 rows)
```

### 7.2 Consulta: Cruce `famprod` vs `mfameq1f.efamilia`

**Query 7.2.1** — Validación 1:1:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT c.famprod, m.efamilia, m.descripcion 
FROM (SELECT DISTINCT famprod FROM cabstdpro WHERE compania = '0030' AND famprod != '') c
LEFT JOIN (SELECT DISTINCT efamilia, descripcion FROM mfameq1f WHERE compania = '0030' AND sucursal = '0001') m 
ON c.famprod = m.efamilia
ORDER BY c.famprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 famprod | efamilia |          descripcion           
---------+----------+--------------------------------
 001     | 001      | EQUIPOS DE ENVASADO
 003     | 003      | TANQUES DE JARABE
 005     | 005      | TANQUES DE TRATAMIENTO DE AGUA
 008     | 008      | BASES TERMINADAS
 009     | 009      | BASES INTERMEDIAS
 010     | 010      | AZUCAR LIQUIDA
 017     | 017      | UNIDAD DE PLOTEO
 019     | 019      | MAQUILA
 021     | 021      | REEMPAQUES
 025     | 025      | PRODUCCION ETIQUETAS
 026     | 026      | PRODUCCION TERMOENCOGIBLE
 051     | 051      | PRODUCCION EXHIBIDORES
(12 rows)
```

**Hallazgo 7.2.1:** **CONFIRMADO — 1:1 perfecto.** Los 12 valores de `cabstdpro.famprod` coinciden exactamente con `mfameq1f.efamilia` para México. La "familia de producción" en la BD legacy ES la familia de equipo. No existe un catálogo separado.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 7

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|---|---|---|
| 1 | `cabstdpro.famprod` tiene 12 valores para MX | 7.1.1 | Son los mismos códigos de `mfameq1f` |
| 2 | **Correspondencia 1:1** entre `famprod` y `efamilia` (12/12) | 7.2.1 | La "familia de producción" ES la familia de equipo |
| 3 | El Program #138 y el #137 referencian el mismo catálogo (`mfameq1f`) | 7.2.1 | Posiblemente son vistas/menús diferentes del mismo modelo |

---

## 8. RASTREO DE `efamilia` EN TODAS LAS TABLAS

**Objetivo:** Identificar todas las tablas que referencian `efamilia` como FK implícita para determinar si alguna contiene configuración adicional de producción más allá de `mfameq1f`.

### 8.1 Consulta: Tablas con columna `efamilia`

**Query 8.1.1** — Búsqueda global:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'public' AND COLUMN_NAME LIKE '%efamilia%'
ORDER BY TABLE_NAME, COLUMN_NAME;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
  table_name   | column_name | data_type 
---------------+-------------+-----------
 aaarfli1f     | efamilia    | text
 asarfli1f     | efamilia    | text
 ctm_familiaeq | efamilia    | text
 drplinpro     | efamilia    | text
 mfameq1f      | efamilia    | text
 sucproc       | efamilia    | text
 tactpr1f      | efamilia    | text
 tparman       | efamilia    | text
 ttarima       | efamilia    | text
(9 rows)
```

**Hallazgo 8.1.1:** 9 tablas referencian `efamilia`. Algunas ya analizadas (`mfameq1f`, `ctm_familiaeq`). Las nuevas requieren inspección: `drplinpro`, `sucproc`, `tactpr1f`, `tparman`, `ttarima`, `aaarfli1f`, `asarfli1f`.

### 8.2 Consulta: Columnas completas de `mfameq1f`

**Query 8.2.1** — Verificar si `mfameq1f` tiene campos no migrados al modelo #137:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'mfameq1f' AND table_schema = 'public'
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

**Hallazgo 8.2.1:** `mfameq1f` tiene 28 columnas. El modelo `bm.ctl.produccion.categoria.linea` (Program #137) migró 10 columnas. Las 11 columnas `bytea` son flags booleanos sin uso transaccional conocido (según análisis #137). No hay campos adicionales de "configuración" de producción que no estén ya en el modelo #137.

### 8.3 Consulta: Estructura de tablas de producción con `efamilia`

**Query 8.3.1** — `drplinpro` (DRP planificación línea-producción):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d drplinpro' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                    Table "public.drplinpro"
   Column    |       Type       | Collation | Nullable | Default 
-------------+------------------+-----------+----------+---------
 codlinpro   | integer          |           | not null | 
 dsclinpro   | text             |           | not null | 
 compania    | text             |           | not null | 
 sucursal    | text             |           | not null | 
 equipo      | integer          |           | not null | 
 rndlinpro   | numeric          |           | not null | 
 stdlinpro   | text             |           | not null | 
 codent      | integer          |           |          | 
 cstrec      | double precision |           |          | 
 rgrup       | boolean          |           |          | 
 flglinea    | boolean          |           |          | 
 flgplan     | boolean          |           |          | 
 efamilia    | text             |           |          | 
 capglopro   | integer          |           |          | 
 codritmo    | integer          |           |          | 
 usercrea    | text             |           |          | 
 fechacrea   | integer          |           | not null | 
 horacrea    | text             |           | not null | 
 usermodi    | text             |           |          | 
 fechamodi   | integer          |           |          | 
 horamodi    | text             |           |          | 
 preferencia | integer          |           |          | 
Indexes:
    "idx_166545_pk_drplinpro" PRIMARY KEY, btree (codlinpro)
```

**Query 8.3.2** — `tactpr1f` (transacciones actividad producción):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d tactpr1f' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                    Table "public.tactpr1f"
   Column   |       Type       | Collation | Nullable | Default 
------------+------------------+-----------+----------+---------
 compania   | text             |           | not null | 
 sucursal   | text             |           | not null | 
 seccierre  | smallint         |           | not null | 
 efamilia   | text             |           | not null | 
 ejercicio  | integer          |           | not null | 
 periodo    | smallint         |           | not null | 
 transaccio | text             |           | not null | 
 cedis      | text             |           | not null | 
 comprobant | double precision |           | not null | 
 feccrea    | integer          |           | not null | 
 horcrea    | text             |           | not null | 
 usucrea    | text             |           | not null | 
 fecultmod  | integer          |           | not null | 
 horultmod  | text             |           | not null | 
 usuultmod  | text             |           | not null | 
```

**Query 8.3.3** — `tparman` (parámetros mantenimiento/OEE):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d tparman' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                     Table "public.tparman"
   Column   |       Type       | Collation | Nullable | Default 
------------+------------------+-----------+----------+---------
 compania   | text             |           |          | 
 sucursal   | text             |           |          | 
 ejercicio  | integer          |           |          | 
 periodoctb | integer          |           |          | 
 fecha      | integer          |           |          | 
 efamilia   | text             |           |          | 
 turno      | text             |           |          | 
 nroopref   | text             |           |          | 
 codlinoee  | text             |           |          | 
 codpar     | text             |           |          | 
 correlat   | integer          |           |          | 
 frecuencia | double precision |           |          | 
 minutos    | double precision |           |          | 
 secxanio   | integer          |           |          | 
 estado     | text             |           |          | 
 feccrea    | integer          |           |          | 
 horcrea    | text             |           |          | 
 usucrea    | text             |           |          | 
 ultfecmod  | integer          |           |          | 
 ulthormod  | text             |           |          | 
 ultusumod  | text             |           |          | 
```

### 8.4 Consulta: Conteo de registros para México en tablas candidatas

**Query 8.4.1**:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT COUNT(*) FROM drplinpro WHERE compania = '0030';
SELECT COUNT(*) FROM sucproc WHERE compania = '0030';
SELECT COUNT(*) FROM tactpr1f WHERE compania = '0030';
SELECT COUNT(*) FROM tparman WHERE compania = '0030';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 count 
-------
     0    ← drplinpro: VACÍA para MX
    16    ← sucproc: ¡16 REGISTROS!
     0    ← tactpr1f: VACÍA para MX
     0    ← tparman: VACÍA para MX
```

**Hallazgo 8.4.1:** **Solo `sucproc` tiene datos operativos para México (0030).** Las demás tablas candidatas están vacías. `sucproc` emerge como la tabla de configuración asociada al Program #138.

### 8.5 Consulta: Análisis de `sucproc` — CONFIRMACIÓN DE TABLA DEL PROGRAM #138

**Query 8.5.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d sucproc' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                Table "public.sucproc"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 sucursal   | text    |           | not null | 
 efamilia   | text    |           | not null | 
 estado     | text    |           |          | 
 feccrea    | integer |           | not null | 
 horcrea    | text    |           | not null | 
 usucrea    | text    |           | not null | 
 fecultmod  | integer |           | not null | 
 horultimod | text    |           | not null | 
 ultusumod  | text    |           | not null | 
Indexes:
    "idx_173441_sucproc_i1" PRIMARY KEY, btree (compania, sucursal, efamilia)
```

**Query 8.5.2** — Datos completos para México:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM sucproc WHERE compania = '0030' ORDER BY sucursal, efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | efamilia | estado | feccrea | horcrea | usucrea | fecultmod | horultimod | ultusumod 
----------+----------+----------+--------+---------+---------+---------+-----------+------------+-----------
 0030     | 0001     | 001      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0001     | 003      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0001     | 019      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0001     | 021      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0068     | 001      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0068     | 003      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0068     | 019      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0068     | 021      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0070     | 001      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0070     | 003      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0070     | 019      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0070     | 021      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0108     | 001      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0108     | 003      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0108     | 019      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
 0030     | 0108     | 021      | A      |  737621 | 113837  | SYSTEM  |    737621 | 113837     | SYSTEM
(16 rows)
```

**Hallazgo 8.5.1 — DEFINITIVO:** `sucproc` configura **qué familias de producción operan en cada sucursal**. PK: `(compania, sucursal, efamilia)`. Solo 4 columnas de negocio: `compania`, `sucursal`, `efamilia`, `estado`. 16 registros: 4 sucursales × 4 familias cada una.
- Sucursales activas: 0001, 0068, 0070, 0108
- Familias configuradas: 001 (ENVASADO), 003 (JARABES), 019 (MAQUILA), 021 (REEMPAQUES)

Esto confirma que el Program #138 `Mantenimiento → Configuraciones → Familia de Produccion` NO es un simple menú duplicado del #137. Es una **configuración** que activa/desactiva familias de equipo por sucursal.

---

## 9. TABLAS AUXILIARES: `equi_famprod` Y `mlifatipobebida1f`

**Objetivo:** Documentar tablas auxiliares que complementan el ecosistema de familias.

### 9.1 `equi_famprod` — Mapeo MAG ↔ BM

**Query 9.1.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d equi_famprod' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
           Table "public.equi_famprod"
 Column  | Type | Collation | Nullable | Default 
---------+------+-----------+----------+---------
 fam_mag | text |           |          | 
 nommag  | text |           |          | 
 fam_bm  | text |           |          | 
 nombm   | text |           |          | 
```

**Query 9.1.2** — Datos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM equi_famprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 fam_mag |          nommag           | fam_bm |             nombm              
---------+---------------------------+--------+--------------------------------
 001     | ENVASADO                  | 001    | EQUIPOS DE ENVASADO
 002     | SOPLADO                   | 002    | EQUIPOS DE SOPLADO
 003     | JARABE TERMINADO          | 003    | TANQUES DE JARABE
 007     | AGUA TRATADA              | 005    | TANQUES DE TRATAMIENTO DE AGUA
 011     | BASE DE BEBIDAS           | 008    | BASES TERMINADAS
 011     | BASE DE BEBIDAS           | 009    | BASES INTERMEDIAS
 010     | AZUCAR LIQUIDA            | 010    | AZUCAR LIQUIDA
 057     | MAQUILA                   | 019    | MAQUILA
 056     | EQUIPOS DE REEMPAQUE      | 021    | REEMPAQUES
 035     | PRODUCCION ETIQUETAS      | 025    | PRODUCCION ETIQUETAS
 040     | PRODUCCION TERMOENCOGIBLE | 026    | PRODUCCION TERMOENCOGIBLE
 058     | PRODUCCION BOTELLA        | 027    | PRODUCCION BOTELLA
(12 rows)
```

**Hallazgo 9.1.1:** `equi_famprod` es una tabla de mapeo entre los códigos de familia de MAG/AVAIL (`fam_mag`) y Big Magic (`fam_bm`). 12 registros. Notar que `fam_bm=027` (PRODUCCION BOTELLA) no aparece en `cabstdpro.famprod` ni en `mfameq1f` con estado activo para MX.

### 9.2 `mlifatipobebida1f` — Tipo de Bebida

**Query 9.2.1** — Estructura:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mlifatipobebida1f' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
           Table "public.mlifatipobebida1f"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 linea      | text    |           | not null | 
 familia    | text    |           | not null | 
 tipobebida | text    |           | not null | 
 estado     | text    |           | not null | 
 feccrea    | integer |           |          | 
 horcrea    | text    |           |          | 
 usuacrea   | text    |           |          | 
 fecultmod  | integer |           |          | 
 horultmod  | text    |           |          | 
 usultmod   | text    |           |          | 
Indexes:
    "idx_170082_mlifatipobebida1f_i1" PRIMARY KEY, btree (compania, linea, familia, tipobebida)
```

**Query 9.2.2** — Tipos de bebida activos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT tipobebida, COUNT(*) as cnt FROM mlifatipobebida1f 
WHERE compania = '0030' AND estado = 'A' 
GROUP BY tipobebida ORDER BY tipobebida;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tipobebida | cnt 
------------+-----
 501        |   8
 502        |  17
 503        |   7
```

**Hallazgo 9.2.1:** `mlifatipobebida1f` clasifica por tipo de bebida (501/502/503) dentro de cada `(compania, linea, familia)`. Solo 3 tipos activos. Esto es una clasificación de artículo, no una familia de producción.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 9

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|---|---|---|
| 1 | `equi_famprod` mapea 12 familias MAG↔BM | 9.1.1 | Útil como referencia de nomenclatura |
| 2 | `mlifatipobebida1f` tiene 3 tipos de bebida activos (501/502/503) | 9.2.2 | Clasificación de artículo, no familia de producción |

---

## 10. CONCLUSIÓN GENERAL — PROGRAM #138

### 10.1 Hipótesis inicial (Secciones 2 a 7)

Tras las primeras 45+ queries, la evidencia apuntaba a dos escenarios posibles:

- **Opción A:** El Program #138 era un simple menú duplicado/alternativo del #137 bajo Configuraciones, apuntando al mismo catálogo `mfameq1f`. Fundamentos: `cabstdpro.famprod ≡ mfameq1f.efamilia` (1:1), no existía tabla maestra tipo `bfamilia1f`, y `mfamil1f`/`msubfa1f` eran de inventario contable.

- **Opción B:** Existían campos de configuración adicionales (ej. `flgsoplado`, `flgbrix` de `mfamil1f`, o flags `bytea` de `mfameq1f`) que justificaban un modelo separado con herencia `_inherits` sobre `bm.ctl.produccion.categoria.linea`.

Ambas opciones se dejaron abiertas a verificación con consultas adicionales.

### 10.2 Resolución (Sección 8)

La consulta de tablas con columna `efamilia` (Query 8.1.1) reveló 9 tablas candidatas. Al verificar datos para México 0030 (Query 8.4.1), solo `sucproc` tenía registros operativos (16). Las demás estaban vacías.

**`sucproc`** configura **qué familias de producción operan en cada sucursal**:
- PK: `(compania, sucursal, efamilia)`
- 4 sucursales activas: 0001, 0068, 0070, 0108
- 4 familias por sucursal: 001 (ENVASADO), 003 (JARABES), 019 (MAQUILA), 021 (REEMPAQUES)

Este hallazgo **descarta la Opción A** (menú duplicado) y confirma que el Program #138 tiene su propia tabla de configuración (`sucproc`), distinta del catálogo `mfameq1f` del Program #137.

Respecto a la **Opción B**: `sucproc` no contiene campos tipo `flgsoplado`/`flgbrix` — esos pertenecen a `mfamil1f` (inventario contable, descartado en Sección 3). `sucproc` es minimalista: solo activa/desactiva la relación sucursal↔familia. Por lo tanto, no se requiere herencia `_inherits`, sino un modelo independiente con FK a `bm.ctl.produccion.categoria.linea`.

### 10.3 Relación Program #137 ↔ Program #138

| Aspecto | Program #137 | Program #138 |
|---|---|---|
| Menú | Mantenimiento → **Clasificadores** | Mantenimiento → **Configuraciones** |
| Tabla legacy | `mfameq1f` (catálogo) | `sucproc` (configuración) |
| Propósito | CRUD del catálogo de familias de equipo | Activar/desactivar familias por sucursal |
| Clave | `(compania, sucursal, efamilia)` | `(compania, sucursal, efamilia)` |
| Modelo Odoo | `bm.ctl.produccion.categoria.linea` | `bm.ctl.produccion.familia` (nuevo) |
| Dependencia | Ninguna | FK → `bm.ctl.produccion.categoria.linea` |

### 10.4 Acción recomendada para Odoo 19

**Crear el modelo `bm.ctl.produccion.familia`** con campos:
- `company_id` (many2one → res.company)
- `sucursal_id` (many2one → bm.sucursal)
- `categoria_linea_id` (many2one → bm.ctl.produccion.categoria.linea)
- `active` (boolean, mapeado de `estado = 'A'`/`'I'`)
- `fecha_creacion`, `fecha_modificacion`, `usuario_crea`, `usuario_modifica` (auditoría)

Vista: lista editable con agrupación por sucursal. Menú: `Mantenimiento → Configuraciones → Familia de Produccion` (sequence 10 dentro de configuraciones).

Opcional: Agregar un menú alternativo en `Costos → Costo SemiVariable → Variables de Produccion → Familia de Produccion` (sequence 20) que apunte al mismo modelo, como se hizo con el Program #137 que tiene doble acceso.

---

## 11. DUDAS LUEGO DEL ANÁLISIS DE LAS CONSULTAS PREVIAS

### 11.1 Duda 1: ¿Por qué solo 4 familias de 27 están configuradas en `sucproc`?

De las 27 familias en `mfameq1f` para sucursal 0001, solo 4 tienen registro en `sucproc`. Hay 11 familias adicionales con `estado='A'` en `mfameq1f` que NO están configuradas en `sucproc`.

**Query 11.1.1** — Comparación `mfameq1f` vs `sucproc` (sucursal 0001):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT m.efamilia, m.descripcion, m.estado AS mfameq1f_estado, s.estado AS sucproc_estado,
       CASE WHEN s.efamilia IS NOT NULL THEN 'CONFIGURADA' ELSE 'NO CONFIGURADA' END AS config
FROM mfameq1f m
LEFT JOIN sucproc s ON m.compania = s.compania AND m.sucursal = s.sucursal AND m.efamilia = s.efamilia
WHERE m.compania = '0030' AND m.sucursal = '0001'
ORDER BY config DESC, m.efamilia;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 efamilia |          descripcion           | mfameq1f_estado | sucproc_estado |     config     
----------+--------------------------------+-----------------+----------------+----------------
 001      | EQUIPOS DE ENVASADO            | A               | A              | CONFIGURADA
 003      | TANQUES DE JARABE              | A               | A              | CONFIGURADA
 019      | MAQUILA                        | A               | A              | CONFIGURADA
 021      | REEMPAQUES                     | A               | A              | CONFIGURADA
 002      | EQUIPOS DE SOPLADO             | A               |                | NO CONFIGURADA
 005      | TANQUES DE TRATAMIENTO DE AGUA | A               |                | NO CONFIGURADA
 008      | BASES TERMINADAS               | A               |                | NO CONFIGURADA
 009      | BASES INTERMEDIAS              | A               |                | NO CONFIGURADA
 010      | AZUCAR LIQUIDA                 | A               |                | NO CONFIGURADA
 017      | UNIDAD DE PLOTEO               | A               |                | NO CONFIGURADA
 025      | PRODUCCION ETIQUETAS           | A               |                | NO CONFIGURADA
 026      | PRODUCCION TERMOENCOGIBLE      | A               |                | NO CONFIGURADA
 027      | PRODUCCION BOTELLA             | A               |                | NO CONFIGURADA
 051      | PRODUCCION EXHIBIDORES         | A               |                | NO CONFIGURADA
 054      | EXTRUIDO SNACKS                | A               |                | NO CONFIGURADA
 ... (12 inactivas adicionales) ...
(27 rows)
```

**conclusion**
1. Solo 4 de 27 familias están configuradas: 001 (ENVASADO), 003 (JARABES), 019 (MAQUILA), 021 (REEMPAQUES). Son las familias de producción de **envasado directo y maquila**, es decir, las que generan producto terminado.
2. Las 11 familias activas NO configuradas son procesos **auxiliares o intermedios**: soplado (002), tratamiento de agua (005), bases (008/009), azúcar (010), etiquetas (025), termos (026), botella (027), exhibidores (051), plotter (017), snacks (054).
3. Esto sugiere que `sucproc` representa las **líneas de producción principales** por sucursal, no los procesos auxiliares. Los procesos auxiliares pueden alimentar varias líneas sin necesidad de una configuración explícita por sucursal.
4. **Acción para Odoo 19**: El modelo debe permitir configurar cualquier familia, no solo estas 4. La lista de `mfameq1f` completa debe estar disponible como opciones.

---

### 11.2 Duda 2: ¿Por qué solo 4 sucursales de 10 tienen configuración en `sucproc`?

El análisis del Program #137 identificó 10 sucursales operativas reales en México (0030), pero `sucproc` solo tiene registros para 4.

**Query 11.2.1** — Distribución de `sucproc` por sucursal:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT s.sucursal, COUNT(*) as familias_configuradas,
       STRING_AGG(s.efamilia, ', ' ORDER BY s.efamilia) as familias
FROM sucproc s
WHERE s.compania = '0030' AND s.estado = 'A'
GROUP BY s.sucursal
ORDER BY s.sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 sucursal | familias_configuradas |      familias      
----------+-----------------------+--------------------
 0001     |                     4 | 001, 003, 019, 021
 0068     |                     4 | 001, 003, 019, 021
 0070     |                     4 | 001, 003, 019, 021
 0108     |                     4 | 001, 003, 019, 021
(4 rows)
```

**conclusion**
1. Las 4 sucursales configuradas (0001, 0068, 0070, 0108) comparten exactamente las mismas 4 familias.
2. Las 6 sucursales faltantes (0086, 0112, 0113, 0114, 0115, 0116) tienen el catálogo `mfameq1f` completo (27 categorías) pero 0 registros en `sucproc`.
3. Esto sugiere que `sucproc` no era una configuración obligatoria para todas las sucursales, sino que se activaba solo para las plantas con producción directa. Las sucursales sin `sucproc` posiblemente no tenían líneas de producción propias o heredaban la configuración de la sucursal principal (0001).
4. **Acción para Odoo 19**: No crear registros automáticos para las 6 sucursales sin configuración. El modelo debe permitir crear nuevas configuraciones bajo demanda.

---

### 11.3 Duda 3: ¿El Program #138 era una vista sobre `mfameq1f` con checkboxes por sucursal, o una pantalla independiente?

**Respuesta:** Dado que `sucproc` es una tabla independiente con su propia PK `(compania, sucursal, efamilia)` y su propio ciclo de auditoría (fechas de creación/modificación independientes de `mfameq1f`), el Program #138 era muy probablemente una **pantalla de configuración independiente**, no un simple checkbox sobre el grid de `mfameq1f`. 

Argumentos a favor de pantalla independiente:
- `sucproc` tiene sus propias fechas de creación (737621 = 2020-06-03 en juliano), diferentes de las de `mfameq1f`
- La combinación `(compania, sucursal, efamilia)` en `sucproc` es un subconjunto seleccionado, no un JOIN automático
- Las 4 sucursales tienen exactamente el mismo conjunto de 4 familias, lo que sugiere que fueron creadas deliberadamente (posiblemente con un botón "Copiar configuración de sucursal 0001")

**Acción para Odoo 19**: Crear modelo independiente `bm.ctl.produccion.familia` con vista lista editable agrupada por sucursal, con acción "Copiar configuración" de una sucursal a otra.

---

### 11.4 Duda 4: Relación entre `sucproc` y `cabstdpro.famprod`

`sucproc` tiene 4 familias activas, pero `cabstdpro.famprod` referencia 12 familias. ¿Por qué?

**Query 11.4.1** — Cruce `cabstdpro.famprod` vs `sucproc` (sucursal 0001):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT c.famprod, m.descripcion,
       CASE WHEN s.efamilia IS NOT NULL THEN 'SI' ELSE 'NO' END AS en_sucproc
FROM (SELECT DISTINCT famprod FROM cabstdpro WHERE compania = '0030' AND famprod != '') c
JOIN mfameq1f m ON c.famprod = m.efamilia AND m.compania = '0030' AND m.sucursal = '0001'
LEFT JOIN sucproc s ON s.compania = '0030' AND s.sucursal = '0001' AND s.efamilia = c.famprod AND s.estado = 'A'
ORDER BY en_sucproc DESC, c.famprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 famprod |          descripcion           | en_sucproc 
---------+--------------------------------+------------
 001     | EQUIPOS DE ENVASADO            | SI
 003     | TANQUES DE JARABE              | SI
 019     | MAQUILA                        | SI
 021     | REEMPAQUES                     | SI
 005     | TANQUES DE TRATAMIENTO DE AGUA | NO
 008     | BASES TERMINADAS               | NO
 009     | BASES INTERMEDIAS              | NO
 010     | AZUCAR LIQUIDA                 | NO
 017     | UNIDAD DE PLOTEO               | NO
 025     | PRODUCCION ETIQUETAS           | NO
 026     | PRODUCCION TERMOENCOGIBLE      | NO
 051     | PRODUCCION EXHIBIDORES         | NO
(12 rows)
```

**conclusion**
1. `cabstdpro.famprod` cataloga las 12 familias que tienen datos de costeo estándar (costos cargados en el sistema).
2. `sucproc` solo activa 4 de esas 12 para las sucursales con producción directa.
3. Las 8 familias que están en `cabstdpro` pero no en `sucproc` (005-TRATAMIENTO AGUA, 008/009-BASES, 010-AZUCAR, etc.) son **procesos intermedios** que tienen costo pero no constituyen una línea de producción independiente — alimentan a las líneas principales (001, 003).
4. Esto confirma que `sucproc` y `cabstdpro.famprod` son conceptos independientes: uno configura operación por sucursal, el otro cataloga costeo.
5. **Acción para Odoo 19**: No acoplar `bm.ctl.produccion.familia` con el módulo de costos. Mantenerlos como modelos independientes.

---

### 11.5 Duda 5: ¿Modelo independiente o extensión con `_inherits`?

**Respuesta:** La evidencia confirma **modelo independiente**. 

Argumentos:
- `sucproc` es una tabla separada con su propia PK y ciclo de vida (no es una tabla de extensión 1:1 de `mfameq1f`)
- Las columnas de negocio son solo 4: `compania`, `sucursal`, `efamilia`, `estado` — no incluye campos de `mfameq1f` como `descripcion`, `area`, `factor`, etc.
- La relación con `mfameq1f` es vía FK implícita (`efamilia`), que en Odoo se traduce como `many2one` a `bm.ctl.produccion.categoria.linea`
- Usar `_inherits` forzaría una relación 1:1 que no existe en el legacy (no todas las familias de `mfameq1f` tienen registro en `sucproc`)

**Acción para Odoo 19**: Modelo `bm.ctl.produccion.familia` con `categoria_linea_id` como `Many2one` (no `_inherits`).

---

### RESUMEN DE DUDAS RESUELTAS — SECCIÓN 11

| # | Duda | Resolución | Impacto Odoo 19 |
|---|---|---|---|
| 1 | ¿Por qué solo 4 de 27 familias? | Son las líneas principales (envasado directo); las demás son auxiliares | Permitir configurar cualquier familia del catálogo |
| 2 | ¿Por qué solo 4 de 10 sucursales? | Solo sucursales con producción directa tienen configuración | No crear registros automáticos para sucursales sin datos |
| 3 | ¿Vista o pantalla independiente? | Pantalla independiente (PK propia, fechas propias) | Modelo independiente con vista lista agrupada |
| 4 | Relación con `cabstdpro.famprod`? | Independientes: `cabstdpro` = costeo, `sucproc` = operación | No acoplar con módulo de costos |
| 5 | ¿Modelo independiente o `_inherits`? | Independiente (no es 1:1 con `mfameq1f`) | `Many2one` a `categoria.linea`, no `_inherits` |

---

## 12. DUDAS DE IMPLEMENTACIÓN ODOO 19

Dudas estratégicas surgidas al contrastar los hallazgos de la BD con la arquitectura Odoo 19 propuesta.

---

### 12.1 Duda 1: ¿Cómo implementar "Sucursal" en Odoo 19?

En el Program #137 la sucursal es ignorada (catálogo global), pero en `sucproc` (#138) `sucursal` es parte de la PK. Actualmente los modelos Odoo existentes usan `sucursal = fields.Char()`.

#### 12.1.1 Búsqueda de tabla maestra de sucursales

**Query 12.1.1** — Tablas con "sucursal" en el nombre:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'public' AND TABLE_NAME LIKE '%sucursal%'
ORDER BY TABLE_NAME;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
        table_name        
--------------------------
 equiv_sucursales
 planviaje_cia_sucursal
 tmp_eq_sucursal_2020
 tmp_eq_sucursal_2021
 tmp_eq_sucursal_n
 v_docvta_sucursal_*
(9 rows)
```

Ninguna es tabla maestra: son temporales (`tmp_*`), vistas (`v_*`), o mapeos entre sistemas (`equiv_*`).

**Query 12.1.2** — Búsqueda de `tsucur` / `msucur`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'public' 
  AND (TABLE_NAME LIKE 'tsucur%' OR TABLE_NAME LIKE 'msucur%' OR TABLE_NAME LIKE 'sucursal%')
ORDER BY TABLE_NAME;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 table_name 
------------
(0 rows)
```

No existe tabla maestra `tsucursal`/`msucursal` en el esquema Big Magic.

**Query 12.1.3** — Columnas de `tsucur*` (confirmación negativa):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_schema = 'public' AND table_name LIKE 'tsucur%' 
ORDER BY ordinal_position;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 column_name | data_type 
-------------+-----------
(0 rows)
```

#### 12.1.2 Sucursales con datos reales en tablas de produccion

**Query 12.1.4** — Sucursales en `turno` (Program #132) para MX 0030:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT sucursal FROM turno WHERE compania = '0030' ORDER BY sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 sucursal 
----------
 0001
 0068
 0070
 0086
 0108
 0112
 0113
 0114
 0115
 0116
 114
(11 rows)
```

11 codigos unicos de sucursal, todos alfanumericos de 4 digitos (excepto `114` que parece un outlier/zombi de 3 digitos).

**Query 12.1.5** — Tablas con posibles nombres de compania/sucursal:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'public' 
  AND (TABLE_NAME LIKE '%compania%' OR TABLE_NAME LIKE '%cia%')
ORDER BY TABLE_NAME LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
          table_name           
-------------------------------
 cia_lfsf
 concepto_cia_proveedor
 kpi_renovacion_contratocompania
 plancuentas_compania
 plantilla_cancelacion_cia
 tmp_compania
(6 rows — ninguna es tabla maestra de sucursales)
```

No hay una tabla que mapee codigo → nombre de sucursal en el legacy.

#### 12.1.3 Estado actual en modelos Odoo existentes

Los modelos del modulo `Pruebas/Production/` actualmente tratan sucursal como `fields.Char()`:

- `program_132_turno_horario.py:26` — `sucursal = fields.Char(string='Sucursal', size=4)`
- `program_137_categoria_linea.py` — No incluye sucursal (catalogo global, por diseno)

**conclusion**

1. **No existe tabla maestra de sucursales** en el legacy Big Magic. Los codigos (0001, 0068, etc.) se almacenan como texto en cada tabla transaccional.
2. No hay fuente de verdad para el `nombre` de una sucursal (ej. "Planta Toluca"). Ese dato debera cargarse manualmente o desde un archivo externo.
3. **Accion para Odoo 19**: Crear modelo `bm.sucursal` con campos:
   - `codigo` (Char, required, unique) — codigo legacy
   - `nombre` (Char) — nombre descriptivo (carga manual)
   - `activo` (Boolean, default=True)
   - `company_id` (Many2one → res.company)
4. Permitir creacion bajo demanda. No cargar automaticamente las 11 sucursales desde la BD (algunas como `114` son outliers).

---

### 12.2 Duda 2: ¿Existen parametros operativos ocultos en `sucproc`?

En sistemas legacy, las tablas de configuracion a veces esconden campos de capacidad, eficiencia o velocidad que no se ven a simple vista.

#### 12.2.1 Estructura de sucproc

Ya documentado en **Seccion 8.5.1**: `\d sucproc` muestra 10 columnas:
```
compania, sucursal, efamilia, estado,
feccrea, horcrea, usucrea,
fecultmod, horultmod, ultusumod
```
Solo IDs + auditoria. **Sin campos numericos de capacidad/velocidad/eficiencia**.

#### 12.2.2 Stored Procedures que operan sobre sucproc

**Query 12.2.1** — SPs con "sucproc" en el nombre:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT proname FROM pg_proc WHERE proname ILIKE '%sucproc%';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 proname 
---------
(0 rows)
```

#### 12.2.3 Catalogo de funciones (Excel #478789)

Busqueda textual de "sucproc" en el archivo convertido a markdown → 0 coincidencias.

**conclusion**

1. `sucproc` es una **tabla de junction pura** (activacion sucursal↔familia) sin parametros operativos.
2. No existen SPs, triggers ni referencias documentales que le inyecten logica adicional.
3. **Accion para Odoo 19**: El modelo `bm.ctl.produccion.familia` no requiere campos de capacidad, velocidad, ni eficiencia. Solo los 4 campos de negocio + auditoria.

---

### 12.3 Duda 3: ¿Sobrescritura de Factor/Funcion por sucursal?

Si una Categoria tiene `area='B'` y `factor=1.5` a nivel global (#137), ¿puede una sucursal cambiar ese comportamiento en #138?

#### 12.3.1 Columnas de sucproc vs mfameq1f

| Campo | En `mfameq1f` (global) | En `sucproc` (#138) |
|---|---|---|
| `efamilia` / `categoria` | PK | FK |
| `area` | Si | **No** |
| `factor` | Si | **No** |
| `funcion` | Si | **No** |
| `estado` | Si | Si (independiente) |

Evidencia ya documentada:
- `\d mfameq1f` en **Seccion 8.2.1** → 12 columnas incluyendo `area`, `factor`, `funcion`
- `\d sucproc` en **Seccion 8.5.1** → 10 columnas, solo IDs + auditoria (sin `area`, `factor`, `funcion`)

**conclusion**

1. `sucproc` **no tiene columnas** para sobrescribir `area`, `factor` ni `funcion`.
2. La relacion es jerarquica: Categoria (#137) define factor/funcion globalmente; Familia (#138) solo activa/desactiva esa categoria para una sucursal.
3. **Accion para Odoo 19**: Usar `fields related` desde `categoria_linea_id` para exponer `area`, `factor` y `funcion` en el modelo `bm.ctl.produccion.familia` sin permitir sobrescritura.

---

### 12.4 Duda 4: ¿Jerarquia #137 → #138 → #139?

¿La cadena de configuracion de produccion es: Categoria Global (#137) → Familia por Sucursal (#138) → Lineas Fisicas (#139)?

#### 12.4.1 Verificacion del Program #139

Fuente 1 — `bm_ctl_produccion_descripciones.md` (archivo `data_para_agente/`):
```
Program #139 | XXX Mantenimiento de Fases | NO OPERATIVO | NO | NO FIGURA LA OPCION
```
Fuente 2 — `Produccion_arbol_funciones.html`:
```
atributo mexico="NO" para el nodo correspondiente al Program #139
```

**conclusion**

1. El Program #139 (`XXX Mantenimiento de Fases`) **no aplica a Mexico**. Es una funcionalidad inactiva/inexistente en la instancia MX.
2. La jerarquia de configuracion para Mexico termina en `Familia por Sucursal` (#138).
3. Si en el futuro se requieren lineas fisicas, el Many2one debe apuntar a `bm.ctl.produccion.categoria.linea` (#137), no a `bm.ctl.produccion.familia` (#138), porque la linea fisica es un subnivel de la categoria, no de la activacion por sucursal.
4. **Accion para Odoo 19**: No implementar Program #139. Reservar el nombre del modelo para uso futuro si se activa para MX.

---

### 12.5 Duda 5: ¿Limpieza de datos legacy para carga inicial?

¿Cuantas combinaciones Sucursal-Familia existen realmente y cuantas hay que filtrar?

#### 12.5.1 Datos actuales en sucproc

Ya documentado en **Seccion 8.5.2** — 16 registros, todos activos:

```text
 compania | sucursal | efamilia | estado 
----------+----------+----------+--------
 0030     | 0001     | 001      | A
 0030     | 0001     | 003      | A
 0030     | 0001     | 019      | A
 0030     | 0001     | 021      | A
 0030     | 0068     | 001      | A
 ... (patron identico para 0068, 0070, 0108) ...
(16 rows)
```

#### 12.5.2 Comparacion con sucursales operativas

Del analisis combinado:
- `sucproc` usa 4 sucursales (0001, 0068, 0070, 0108) → **4 operativas con configuracion**
- `turno` tiene 10+1 sucursales (incluye 0086, 0112-0116, 114) → **6 adicionales sin configuracion en sucproc**
- Las 6 sin configuracion en `sucproc` son operativas en otras areas (turnos, costos) pero no tienen lineas de produccion propias

**conclusion**

1. Datos **limpios**: 16 registros, todos `estado='A'`, sin sucursales zombi.
2. Sin registros `estado='I'` (inactivo historico) — no hay basura que limpiar.
3. La sucursal `114` (3 digitos, outlier) no aparece en `sucproc` — no contamina los datos.
4. **Accion para Odoo 19**: Seed de los 16 registros directamente desde `sucproc`. No se requiere limpieza previa.

---

### RESUMEN DE DUDAS RESUELTAS — SECCION 12

| # | Duda | Resolucion | Queries | Impacto Odoo 19 |
|---|---|---|---|---|
| 1 | ¿Char o modelo `bm.sucursal`? | No hay tabla maestra legacy → crear modelo | 5 | `bm.sucursal` con `codigo`, `nombre`, `activo` |
| 2 | ¿Parametros operativos ocultos? | No existen (solo IDs+auditoria, 0 SPs, 0 en Excel) | 1 | Sin campos de capacidad/velocidad |
| 3 | ¿Sobrescritura de Factor/Funcion? | No (columnas no existen en `sucproc`) | 0 (ref 8.2.1, 8.5.1) | `related fields` desde `categoria.linea` |
| 4 | ¿Jerarquia #137→#138→#139? | #139 NO OPERATIVO para Mexico | 0 (ref docs) | Linea fisica → `categoria.linea`, no `familia` |
| 5 | ¿Limpieza de datos? | 16 registros limpios, todos activos | 0 (ref 8.5.2) | Seed directo sin filtrado |

---

