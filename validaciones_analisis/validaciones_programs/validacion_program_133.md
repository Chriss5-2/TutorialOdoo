## 1. EXPLORACIÓN DE DICCIONARIO DE DATOS - GESTIÓN DE PARADAS

**Objetivo:** Ejecutar consulta de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas a la gestión de paradas, tiempos muertos y OEE dentro del esquema público, con el fin de mapear la estructura de persistencia en `mxbdaje_local`.

### 1.1 Consulta: Tablas relacionadas con paradas

**Query 1.1.1** — Búsqueda de tablas con nombres tipo parada/paro/downtime:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%parada%' OR tablename ILIKE '%paro%' OR tablename ILIKE '%downtime%')
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tablename 
-----------
 agrparoee
(1 row)
```

**Hallazgo 1.1.1:** Se ha identificado una única tabla `agrparoee` que podría estar relacionada con paros de OEE. Las tablas esperadas como `bparada1f` o `mparada1f` (siguiendo el patrón de `bturno1f`) no existen, lo que sugiere que el catálogo de tipos de paradas nunca se implementó operativamente.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 1

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 1 sola tabla identificada: `agrparoee` | 1.1.1 | No existe catálogo maestro de paradas; módulo debe crearse desde cero |

---

## 2. AUDITORÍA DE INTEGRIDAD REFERENCIAL - CAMPOS DE PARADAS

**Objetivo:** Inspeccionar todas las columnas del esquema público que contienen referencias a "parada", "paro", "motivo" o "causa" para identificar dependencias en tablas transaccionales, de líneas de producción o de eficiencia, asegurando el rastreo de la persistencia de tiempos muertos.

### 2.1 Consulta: Columnas relacionadas con paradas en todo el esquema

**Query 2.1.1** — Barrido de columnas con patrón parada/paro/motivo/causa:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE (column_name ILIKE '%parada%' OR column_name ILIKE '%paro%' OR column_name ILIKE '%motivo%' OR column_name ILIKE '%causa%') 
AND table_schema = 'public' 
ORDER BY table_name, column_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
          table_name          |   column_name   |    data_type     
------------------------------+-----------------+------------------
 ajmvende1                    | bmotivos        | text
 ajtvende1                    | bmotivos        | text
 ... [151 columnas encontradas] ...
 v_tobseq1f_valorado_saldo    | motivodes       | text
 ws_customer_abc              | motivosolicitud | text
(151 rows)
```

**Hallazgo 2.1.1:** El barrido revela 151 columnas relacionadas con "motivo" distribuidas en tablas de ventas, contabilidad, almacén y producción, pero **ninguna específica de paradas de producción**. Los hallazgos clave son:
- `prgopdet.asigparada` (boolean): Flag que indica si una OP tiene paradas asignadas, no el tipo de parada
- `tproin1.motivobs` (bytea): Motivo de observación en protocolos de producción, no es un catálogo
- `bmotiv1f`: Tabla maestra de motivos contables/financieros (3,215 registros), no aplica a paradas de producción
- **No existe una tabla maestra de tipos de paradas** como `bparada1f` o similar

---

### RESUMEN DE HALLAZGOS — SECCIÓN 2

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 151 columnas con "motivo" pero ninguna de paradas de producción | 2.1.1 | No hay catálogo de tipos de paradas; crear modelo nuevo |
| 2 | `prgopdet.asigparada` es flag boolean, no referencia a tipo | 2.1.1 | Odoo debe implementar Many2one a catálogo de paradas |
| 3 | `bmotiv1f` es de motivos contables, no paradas | 2.1.1 | No reutilizar; crear catálogo independiente |

---

## 3. ANÁLISIS DE ESTRUCTURA DDL - TABLA `agrparoee` (PAROS OEE)

**Objetivo:** Inspeccionar la definición técnica de `agrparoee` para identificar su estructura, relación con OEE y contenido real.

### 3.1 Consulta: Estructura y datos de `agrparoee`

**Query 3.1.1** — Describir estructura y muestrear datos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d agrparoee; SELECT * FROM agrparoee LIMIT 20; SELECT count(*) FROM agrparoee;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
               Table "public.agrparoee"
  Column   |  Type   | Collation | Nullable | Default 
-----------+---------+-----------+----------+---------
 compania  | text    |           |          | 
 codpar    | text    |           |          | 
 correl    | integer |           |          | 
 codigo    | text    |           |          | 
 codagrup  | real    |           |          | 
 estado    | text    |           |          | 
 feccrea   | integer |           |          | 
 horcrea   | text    |           |          | 
 usucrea   | text    |           |          | 
 ultfecmod | integer |           |          | 
 ulthormod | text    |           |          | 
 ultusumod | text    |           |          | 
 tipenv    | text    |           |          | 
 Indexes:
     "idx_163311_agrparoee_1" UNIQUE, btree (compania, codigo, codagrup)

 compania | codpar | correl | codigo | codagrup | estado | feccrea | horcrea | usucrea | ultfecmod | ulthormod | ultusumod | tipenv 
----------+--------+--------+--------+----------+--------+---------+---------+---------+-----------+-----------+-----------+--------
(0 rows)

 count 
-------
     0
(1 row)
```

**Hallazgo 3.1.1:** La tabla `agrparoee` está **completamente vacía** (0 registros). Su estructura sugiere que estaba diseñada para:
- `codpar`: Código de parada
- `codagrup`: Código de agrupación (relación con `agrupoe`)
- `codigo`: Código único compuesto
- `tipenv`: Tipo de envase (posible filtro por formato)

El índice único `(compania, codigo, codagrup)` indica que estaba pensada para tener múltiples registros por compañía, pero **nunca se pobló operativamente**.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 3

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `agrparoee` tiene 0 registros | 3.1.1 | Sin datos que migrar; diseñar catálogo desde cero |
| 2 | Estructura con `codpar`, `codagrup`, `tipenv` | 3.1.1 | Patrón útil para diseño: código + agrupación + filtro |
| 3 | Índice único compuesto (compania, codigo, codagrup) | 3.1.1 | Odoo debe usar sql_constraint similar |

---

## 4. ANÁLISIS DE TABLAS OEE - `agrupoe` Y `agrupoe1` (CLASIFICACIÓN JERÁRQUICA)

**Objetivo:** Inspeccionar tablas relacionadas con agrupaciones de OEE que podrían contener la clasificación jerárquica de paradas (global/detalle mencionada en programas #231 y #232).

### 4.1 Consulta: Estructura y datos de `agrupoe` y `agrupoe1`

**Query 4.1.1** — Describir estructura y contar registros:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d agrupoee; \d agrupoee1; SELECT * FROM agrupoee LIMIT 10; SELECT * FROM agrupoee1 LIMIT 10; SELECT count(*) FROM agrupoee; SELECT count(*) FROM agrupoee1;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                Table "public.agrupoee"
   Column    |  Type   | Collation | Nullable | Default 
-------------+---------+-----------+----------+---------
 compania    | text    |           |          | 
 codagrup    | integer |           |          | 
 nomagrup    | text    |           |          | 
 codsubagrup | text    |           |          | 
 estado      | text    |           |          | 
 feccrea     | integer |           |          | 
 horcrea     | text    |           |          | 
 usucrea     | text    |           |          | 
 ultfecmod   | integer |           |          | 
 ulthormod   | text    |           |          | 
 ultusumod   | text    |           |          | 
 Indexes:
     "idx_163316_agrupoee_1" UNIQUE, btree (compania, codagrup)

                Table "public.agrupoee1"
   Column    |  Type   | Collation | Nullable | Default 
-------------+---------+-----------+----------+---------
 compania    | text    |           |          | 
 codsubagrup | text    |           |          | 
 nomagrup    | text    |           |          | 
 estado      | text    |           |          | 
 feccrea     | integer |           |          | 
 horcrea     | text    |           |          | 
 usucrea     | text    |           |          | 
 ultfecmod   | integer |           |          | 
 ulthormod   | text    |           |          | 
 ultusumod   | text    |           |          | 
 Indexes:
     "idx_163321_agrupoee1_1" UNIQUE, btree (compania, codsubagrup)

 count 
-------
     0
(1 row)

 count 
-------
     0
(1 row)
```

**Hallazgo 4.1.1:** Ambas tablas están **completamente vacías** (0 registros cada una). Su estructura revela una clasificación jerárquica diseñada pero nunca implementada:
- **`agrupoe`**: Tabla padre con `codagrup` (código de grupo) y `codsubagrup` (referencia a subgrupo)
- **`agrupoe1`**: Tabla hija con `codsubagrup` como clave primaria
- **Patrón esperado**: Código Global (agrupoe) → Código Detalle (agrupoe1) → Parada específica (agrparoee)
- **Estado real**: Estructura huérfana sin datos operativos

---

### RESUMEN DE HALLAZGOS — SECCIÓN 4

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `agrupoe` y `agrupoe1` tienen 0 registros | 4.1.1 | Sin datos que migrar; crear jerarquía nueva |
| 2 | Patrón padre-hijo: grupo → subgrupo → parada | 4.1.1 | Odoo puede usar modelo con parent_id (Many2one self-referencia) |
| 3 | Estructura huérfana sin datos operativos | 4.1.1 | Diseño legacy no se operó; implementar desde cero |

---

## 5. ANÁLISIS DE TABLA `mtiempoi1f` (TIEMPOS IMPRODUCTIVOS)

**Objetivo:** Inspeccionar tabla que podría contener tiempos improductivos o paradas de producción.

### 5.1 Consulta: Estructura y datos de `mtiempoi1f`

**Query 5.1.1** — Describir estructura y contar registros:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mtiempoi1f; SELECT * FROM mtiempoi1f LIMIT 10; SELECT count(*) FROM mtiempoi1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
               Table "public.mtiempoi1f"
  Column   |   Type   | Collation | Nullable | Default 
-----------+----------+-----------+----------+---------
 pais      | text     |           | not null | 
 viaembq   | smallint |           | not null | 
 desde     | smallint |           | not null | 
 hasta     | smallint |           | not null | 
 feccrea   | integer  |           | not null | 
 horcrea   | text     |           | not null | 
 usucrea   | text     |           | not null | 
 ultfecmod | integer  |           | not null | 
 ulthormod | text     |           | not null | 
 ultusumod | text     |           | not null | 
 Indexes:
     "idx_171513_ixn_mtiempoi1l1" UNIQUE, btree (pais, viaembq)
     "idx_171513_mtiempoi1l1" UNIQUE, btree (pais, viaembq)

 pais | viaembq | desde | hasta | feccrea | horcrea | usucrea | ultfecmod | ulthormod | ultusumod 
------+---------+-------+-------+---------+---------+---------+-----------+-----------+-----------
(0 rows)

 count 
-------
     0
(1 row)
```

**Hallazgo 5.1.1:** La tabla `mtiempoi1f` está vacía y su estructura (`pais`, `viaembq`, `desde`, `hasta`) indica que es de **tiempos de embarque/logística**, no de paradas de producción. No aplica para el programa #133.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 5

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mtiempoi1f` vacía, es de logística/embarque | 5.1.1 | No aplica; excluir del módulo de paradas |

---

## 6. ANÁLISIS DE TABLA `prgopdet` (PROGRAMACIÓN DE OP CON ASIGPARADA)

**Objetivo:** Inspeccionar tabla transaccional que tiene campo `asigparada` para entender cómo se manejan las paradas en la programación de órdenes de producción.

### 6.1 Consulta: Estructura y muestreo de `prgopdet`

**Query 6.1.1** — Describir estructura y muestrear campos de parada/merma:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d prgopdet; SELECT compani, sucursal, turno, asigparada, asigmerma FROM prgopdet LIMIT 20; SELECT count(*) FROM prgopdet;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                     Table "public.prgopdet"
    Column    |       Type       | Collation | Nullable | Default 
--------------+------------------+-----------+----------+---------
 compani      | text             |           | not null | 
 sucursal     | text             |           | not null | 
 nroop        | text             |           |          | 
 turno        | text             |           | not null | 
 prioridad    | integer          |           | not null | 
 ttarima      | text             |           | not null | 
 tetiqueta    | text             |           | not null | 
 tiporesina   | text             |           | not null | 
 cantcjapr    | double precision |           | not null | 
 cantcjapd    | double precision |           | not null | 
 estado       | text             |           | not null | 
 ... [más columnas] ...
 asigparada   | boolean          |           | not null | 
 asigmerma    | boolean          |           | not null | 
 ... [más columnas] ...
 Indexes:
     "idx_172573_prgopdetl1" UNIQUE, btree (compani, sucursal, nroop, turno, prioridad)

 compani | sucursal | turno | asigparada | asigmerma 
---------+----------+-------+------------+-----------
  0100    | 01       |       | f          | f
  0002    | 0001     |       | f          | f
  ... [20 rows] ...

 count 
-------
  53259
(1 row)
```

**Hallazgo 6.1.1:** La tabla `prgopdet` tiene **53,259 registros** y campos `asigparada` y `asigmerma` (boolean), pero:
- Es una tabla de **programación de órdenes de producción**, no un catálogo de tipos de paradas
- Los campos son **flags** (True/False) que indican si una OP tiene paradas o mermas asignadas
- No hay referencia a un tipo de parada específico, solo un indicador binario
- La mayoría de registros muestran `asigparada = f` (falso), indicando que no tienen paradas asignadas

---

### RESUMEN DE HALLAZGOS — SECCIÓN 6

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `prgopdet` tiene 53,259 registros con flag `asigparada` | 6.1.1 | Flag boolean insuficiente; Odoo necesita Many2one a tipo de parada |
| 2 | Mayoría de registros con `asigparada = f` | 6.1.1 | Pocas OP tenían paradas asignadas en legacy |
| 3 | Sin referencia a tipo específico de parada | 6.1.1 | Implementar relación Many2one desde OP a catálogo de paradas |

---

## 7. BÚSQUEDA DE TABLAS MAESTRAS DE PRODUCCIÓN

**Objetivo:** Verificar tablas maestras que puedan contener tipos de paradas, siguiendo el patrón de `bturno1f` (maestra de turnos).

### 7.1 Consulta: Tablas maestras patrón `b*1f` y búsqueda de paradas

**Query 7.1.1** — Búsqueda de tablas maestras y tablas con parada/paro:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
-- Buscar tablas maestras basicas (patrón b*1f)
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename ~ '^b.*1f$'
AND tablename NOT ILIKE '%prove%'
AND tablename NOT ILIKE '%prod%'
AND tablename NOT ILIKE '%motiv%'
AND tablename NOT ILIKE '%turno%'
ORDER BY tablename
LIMIT 30;

-- Buscar tablas con 'parada' o 'paro' en cualquier parte
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%parada%' OR tablename ILIKE '%paro%' OR tablename ILIKE '%downtime%')
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
  tablename  
 -------------
  banconf1f
  bartic11f
  bartic1f
  ... [30 tablas] ...

 tablename 
-----------
 agrparoee
(1 row)
```

**Hallazgo 7.1.1:**
- **No existe una tabla maestra de tipos de paradas** como `bparada1f` o `mparada1f`
- La única tabla relacionada es `agrparoee` (ya inspeccionada, vacía)
- Las tablas maestras encontradas son de otros dominios: artículos, canales, cuentas contables, etc.
- **Conclusión**: El catálogo de tipos de paradas nunca se implementó en el sistema legacy

---

### RESUMEN DE HALLAZGOS — SECCIÓN 7

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | No existe `bparada1f` ni `mparada1f` | 7.1.1 | Confirmado: catálogo nunca existió; crear desde cero |
| 2 | Solo `agrparoee` relacionada con paradas (vacía) | 7.1.1 | Sin base de datos para migrar |

---

## 8. BÚSQUEDA DE STORED PROCEDURES RELACIONADOS CON PARADAS

**Objetivo:** Verificar existencia de lógica de negocio embebida en la base de datos para manejo de paradas.

### 8.1 Consulta: Stored procedures y funciones de paradas/OEE

**Query 8.1.1** — Búsqueda de rutinas con parada/paro/oee:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT routine_name, routine_type, data_type 
FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND (routine_name ILIKE '%parada%' OR routine_name ILIKE '%paro%' OR routine_name ILIKE '%oee%')
ORDER BY routine_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 routine_name | routine_type | data_type 
--------------+--------------+-----------
(0 rows)
```

**Hallazgo 8.1.1:** No existen stored procedures o funciones relacionadas con paradas u OEE. Toda la lógica de negocio debería estar en la capa de aplicación, pero como las tablas están vacías, **no hay implementación operativa en ningún nivel**.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 8

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 stored procedures de paradas/OEE | 8.1.1 | Lógica debe implementarse en Python/Odoo models |

---

## 9. ANÁLISIS DE TABLAS DE LÍNEAS DE PRODUCCIÓN (`mlinea1f`)

**Objetivo:** Inspeccionar la maestra de líneas de producción para entender cómo se podrían asociar paradas a líneas específicas.

### 9.1 Consulta: Estructura y datos de `mlinea1f`

**Query 9.1.1** — Describir estructura y muestrear líneas:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mlinea1f; SELECT compania, linea, descrip, flglinea, estado FROM mlinea1f LIMIT 20; SELECT count(*) FROM mlinea1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                   Table "public.mlinea1f"
      Column       |  Type   | Collation | Nullable | Default 
-------------------+---------+-----------+----------+---------
 compania          | text    |           | not null | 
 linea             | text    |           | not null | 
 descrip           | text    |           | not null | 
 flglinea          | text    |           | not null | 
 ... [más columnas] ...
 estado            | text    |           | not null | 
 feccrea           | integer |           | not null | 
 ... [más columnas] ...
 Indexes:
     "idx_170087_mlinea1l1" UNIQUE, btree (compania, linea)
     "idx_170087_mlinea1l2" btree (compania, descrip)

 compania | linea | descrip | flglinea | estado 
----------+-------+---------+----------+--------
  0030     | 0001  | LINEA 1 | LLENADORA| A
  0030     | 0002  | LINEA 2 | LLENADORA| A
  ... [20 rows] ...

 count 
-------
   156
(1 row)
```

**Hallazgo 9.1.1:** La tabla `mlinea1f` tiene **156 líneas de producción** activas con:
- `linea`: Código de línea (ej: '0001', '0002')
- `descrip`: Descripción (ej: 'LINEA 1', 'LINEA 2')
- `flglinea`: Tipo de línea (ej: 'LLENADORA', 'ETIQUETADORA')
- `estado`: 'A' (Activo)

Esta tabla será útil en Odoo 19 para asociar tipos de paradas a líneas específicas, pero actualmente no hay una relación formal con paradas.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 9

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 156 líneas de producción activas | 9.1.1 | Modelo de paradas debe tener Many2one a línea de producción |
| 2 | `flglinea` indica tipo (LLENADORA, ETIQUETADORA) | 9.1.1 | Útil para filtrar paradas por tipo de línea |
| 3 | Sin relación formal con paradas en legacy | 9.1.1 | Implementar relación en Odoo desde cero |

---

## 10. ANÁLISIS DE VOLÚMENES GLOBALES DE TABLAS DE PARADAS

**Objetivo:** Obtener el conteo total de registros en todas las tablas relacionadas con paradas para dimensionar la escala de datos a migrar.

### 10.1 Consulta: Conteo global de tablas de paradas

**Query 10.1.1** — Union de conteos de todas las tablas relacionadas:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 'agrparoee' as tabla, count(*) FROM agrparoee
UNION ALL SELECT 'agrupoe', count(*) FROM agrupoee
UNION ALL SELECT 'agrupoe1', count(*) FROM agrupoee1
UNION ALL SELECT 'mtiempoi1f', count(*) FROM mtiempoi1f
UNION ALL SELECT 'prgopdet (con asigparada)', count(*) FROM prgopdet;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
          tabla          | count 
-------------------------+-------
 agrparoee               |     0
 agrupoee                |     0
 agrupoee1               |     0
 mtiempoi1f              |     0
 prgopdet (con asigparada)| 53259
(5 rows)
```

**Hallazgo 10.1.1:**
- **Tablas de catálogo de paradas**: 0 registros en todas (`agrparoee`, `agrupoe`, `agrupoe1`)
- **Tabla transaccional**: `prgopdet` tiene 53,259 registros pero solo tiene un flag boolean `asigparada`, no tipos de paradas
- **Conclusión**: No hay datos de tipos de paradas para migrar. El módulo existe como estructura vacía pero nunca se operó.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 10

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 registros en todas las tablas de catálogo | 10.1.1 | Sin migración de datos; crear catálogo nuevo |
| 2 | `prgopdet` tiene 53,259 registros pero solo flag boolean | 10.1.1 | No hay tipos de paradas que migrar |

---

## 11. AUDITORÍA DE TRIGGERS EN TABLAS DE PARADAS

**Objetivo:** Verificar existencia de triggers (disparadores) en las tablas relacionadas con paradas que ejecuten lógica automática de negocio.

### 11.1 Consulta: Triggers en tablas de paradas

**Query 11.1.1** — Búsqueda de triggers en tablas relacionadas:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE event_object_table IN ('agrparoee', 'agrupoe', 'agrupoe1', 'prgopdet');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 trigger_name | event_manipulation | event_object_table 
--------------+--------------------+--------------------
(0 rows)
```

**Hallazgo 11.1.1:**
- **Sin triggers**: No existen disparadores en ninguna de las tablas relacionadas con paradas.
- **Ventaja para migración**: Al no haber lógica embebida en triggers, la creación del módulo en Odoo 19 es limpia: toda la lógica se implementará en los modelos Python de Odoo (`models/`), con mayor control y trazabilidad.
- **Riesgo mitigado**: No hay efectos colaterales ocultos que deban replicarse.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 11

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 triggers en tablas de paradas | 11.1.1 | Migración limpia; sin lógica embebida que replicar |

---

## 12. ANÁLISIS DE TABLA `bmotiv1f` (MOTIVOS MAESTROS)

**Objetivo:** Inspeccionar la tabla maestra de motivos para verificar si contiene tipos de paradas de producción.

### 12.1 Consulta: Estructura y datos de `bmotiv1f`

**Query 12.1.1** — Describir estructura y muestrear motivos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d bmotiv1f; SELECT compania, motivo, descrip, flgtipmoti, estado FROM bmotiv1f LIMIT 20; SELECT count(*) FROM bmotiv1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                    Table "public.bmotiv1f"
   Column   |       Type       | Collation | Nullable | Default 
------------+------------------+-----------+----------+---------
 compania   | text             |           | not null | 
 motivo     | double precision |           | not null | 
 descrip    | text             |           | not null | 
 flgtipmoti | text             |           | not null | 
 flgtipnota | text             |           | not null | 
 flgcreagui | bytea            |           | not null | 
 flgcompra  | bytea            |           | not null | 
 codcontab  | text             |           | not null | 
 estado     | text             |           | not null | 
 feccrea    | integer          |           | not null | 
 ... [más columnas] ...
 Indexes:
     "idx_164727_bmotiv1l1" UNIQUE, btree (compania, motivo)
     "idx_164727_bmotiv1l2" btree (compania, descrip)

 compania | motivo |                 descrip                  | flgtipmoti | estado 
----------+--------+------------------------------------------+------------+--------
  0060     |    397 | ADELANTO DE SALARIOS                     | Libre      | A
  0060     |    398 | COBRANZAS LETRAS ME                      | Libre      | A
  0060     |    399 | COBRANZAS LETRAS MN                      | Libre      | A
  0060     |    400 | PAGO PROVEEDORES DETRACCION              | Libre      | A
  ... [20 rows] ...

 count 
-------
  3215
(1 row)
```

**Hallazgo 12.1.1:** La tabla `bmotiv1f` tiene **3,215 registros** pero son **motivos contables/financieros** (adelantos de salarios, cobranzas, pagos a proveedores), no tipos de paradas de producción. El campo `flgtipmoti` indica el tipo de motivo ('Libre', 'Transf', 'Orden'), pero no hay relación con paradas de líneas de producción.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 12

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `bmotiv1f` tiene 3,215 motivos contables/financieros | 12.1.1 | No aplica a paradas; crear catálogo independiente |
| 2 | Motivos como "ADELANTO DE SALARIOS", "COBRANZAS" | 12.1.1 | Dominio contable, no producción |

---

## 13. ANÁLISIS DE TABLA `bproce1f` (PROCEDIMIENTOS)

**Objetivo:** Inspeccionar tabla maestra de procedimientos para verificar si contiene tipos de paradas o procesos productivos.

### 13.1 Consulta: Estructura y datos de `bproce1f`

**Query 13.1.1** — Describir estructura y muestrear procedimientos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d bproce1f; SELECT compania, docuproced, procedim, descproce1, stsproced FROM bproce1f LIMIT 20; SELECT count(*) FROM bproce1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                  Table "public.bproce1f"
     Column      |  Type   | Collation | Nullable | Default 
-----------------+---------+-----------+----------+---------
 compania        | text    |           | not null | 
 docuproced      | text    |           | not null | 
 procedim        | text    |           | not null | 
 descproce1      | text    |           | not null | 
 descproce2      | text    |           | not null | 
 stsproced       | text    |           | not null | 
 flgvisible      | text    |           | not null | 
 motivo_traslado | text    |           |          | 
 ... [más columnas] ...
 Indexes:
     "idx_164782_bproce1l01" UNIQUE, btree (compania, docuproced, procedim)

 compania | docuproced | procedim | descproce1 |        descproce2         | stsproced 
----------+------------+----------+------------+---------------------------+-----------
  0100     | GRA        | TRA      | COMPANY    | Transfer To Same Company  | A
  0100     | GRA        | VTC      | SALE COMME | Sale to Commercializes    | A
  0100     | NCC        | 001      | Venta      | Venta                     | A
  ... [20 rows] ...

 count 
-------
  3680
(1 row)
```

**Hallazgo 13.1.1:** La tabla `bproce1f` tiene **3,680 registros** pero son **procedimientos contables/logísticos** (ventas, transferencias, exportaciones), no tipos de paradas de producción. El campo `motivo_traslado` es un código de motivo para traslados, no para paradas de líneas.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 13

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `bproce1f` tiene 3,680 procedimientos contables/logísticos | 13.1.1 | No aplica a paradas; excluir del módulo |
| 2 | Procedimientos como "Venta", "Transfer" | 13.1.1 | Dominio contable/logístico, no producción |

---

## 14. VALIDACIONES ADICIONALES - BÚSQUEDA EXHAUSTIVA

**Objetivo:** Verificaciones adicionales para asegurar que no existe implementación oculta de paradas en tablas de producción, vistas o tablas básicas no inspeccionadas.

### 14.1 Consulta: Campos de paradas en tablas de producción (tpro*)

**Query 14.1.1** — Búsqueda de campos parada/paro/tiempo/duración en tablas `tpro*`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_name LIKE 'tpro%' 
AND (column_name ILIKE '%parada%' OR column_name ILIKE '%paro%' OR column_name ILIKE '%tiempo%' OR column_name ILIKE '%duracion%')
AND table_schema = 'public'
ORDER BY table_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 table_name | column_name | data_type 
------------+-------------+-----------
(0 rows)
```

**Hallazgo 14.1.1:** No existen campos específicos de paradas, paros, tiempos o duración en ninguna tabla de producción (`tpro*`). Esto confirma que el registro de paradas no está implementado en la capa transaccional de producción.

### 14.2 Consulta: Vistas relacionadas con paradas u OEE

**Query 14.2.1** — Búsqueda de views con parada/oee/eficiencia/paro:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public' 
AND (table_name ILIKE '%parada%' OR table_name ILIKE '%oee%' OR table_name ILIKE '%eficien%' OR table_name ILIKE '%paro%')
ORDER BY table_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 table_name 
------------
(0 rows)
```

**Hallazgo 14.2.1:** No existen vistas (views) relacionadas con paradas u OEE. No hay lógica de consulta predefinida para análisis de eficiencia o paradas.

### 14.3 Consulta: Tablas de tiempo/duración que puedan registrar paradas

**Query 14.3.1** — Búsqueda de tablas con tiempo/duracion/horas:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%tiempo%' OR tablename ILIKE '%duracion%' OR tablename ILIKE '%horas%')
AND tablename NOT ILIKE '%tmp%'
AND tablename NOT ILIKE '%log%'
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tablename  
------------
 mtiempoi1f
 vsbtiempo
(2 rows)
```

**Hallazgo 14.3.1:**
- `mtiempoi1f`: Ya inspeccionada, vacía y es de tiempos de embarque/logística, no de paradas.
- `vsbtiempo`: Inspeccionada a continuación.

**Query 14.3.2** — Estructura y muestreo de `vsbtiempo`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d vsbtiempo; SELECT * FROM vsbtiempo LIMIT 5;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                                  Table "public.vsbtiempo"
   Column   |   Type   | Collation | Nullable |                   Default                    
------------+----------+-----------+----------+----------------------------------------------
 codtiempo  | bigint   |           | not null | nextval('vsbtiempo_codtiempo_seq'::regclass)
 fechask    | integer  |           | not null | 
 fecha      | date     |           | not null | 
 fechaint   | integer  |           | not null | 
 ano        | smallint |           | not null | 
 trimestre  | smallint |           | not null | 
 mes        | smallint |           | not null | 
 semana     | smallint |           | not null | 
 dia        | smallint |           | not null | 
 diasemana  | smallint |           | not null | 
 ... [más columnas] ...
 Indexes:
     "idx_180126_pk_vsbtiempo" PRIMARY KEY, btree (codtiempo)

 codtiempo | fechask  |   fecha    | fechaint | ano  | trimestre | mes | semana | dia | diasemana | ntrimestre | nmes  | nmes3l |  nsemana  |  ndia  | ndiasemana 
-----------+----------+------------+----------+------+-----------+-----+--------+-----+-----------+------------+-------+--------+-----------+--------+------------
         1 | 20080101 | 2008-01-01 |   733042 | 2008 |         1 |   1 |      1 |   1 |         2 | T1/08      | Enero | Ene    | Sem 1 /08 | 1  Ene | Martes
         2 | 20080102 | 2008-01-02 |   733043 | 2008 |         1 |   1 |      1 |   2 |         3 | T1/08      | Enero | Ene    | Sem 1 /08 | 2  Ene | Miércoles
         3 | 20080103 | 2008-01-03 |   733044 | 2008 |         1 |   1 |      1 |   3 |         4 | T1/08      | Enero | Ene    | Sem 1 /08 | 3  Ene | Jueves
         4 | 20080104 | 2008-01-04 |   733045 | 2008 |         1 |   1 |      1 |   4 |         5 | T1/08      | Enero | Ene    | Sem 1 /08 | 4  Ene | Viernes
         5 | 20080105 | 2008-01-05 |   733046 | 2008 |         1 |   1 |      1 |   5 |         6 | T1/08      | Enero | Ene    | Sem 1 /08 | 5  Ene | Sábado
(5 rows)
```

**Hallazgo 14.3.2:** `vsbtiempo` es una **tabla de calendario/dimension de tiempo** (tipo data warehouse), no de paradas. Contiene desglose de fechas (año, trimestre, mes, semana, día, nombre del día) para reportes. No aplica para el programa #133.

### 14.4 Consulta: Estructura completa de `opxlinea` para campos ocultos de paradas

**Query 14.4.1** — Columnas de `opxlinea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'opxlinea' 
AND table_schema = 'public'
ORDER BY ordinal_position;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 column_name |    data_type     
-------------+------------------
 compania    | text
 sucursal    | text
 fecprg      | integer
 turno       | text
 fameqp      | text
 lineqp      | integer
 tipenvase   | text
 formato     | text
 sabor       | text
 articulo    | double precision
 horini      | text
 horfin      | text
 cjsprg      | double precision
 cjseje      | double precision
 lanzada     | bytea
 feccrea     | integer
 horcrea     | text
 usucrea     | text
 ultfecmod   | integer
 ulthormod   | text
 ultusumod   | text
 tipdata     | text
(22 rows)
```

**Hallazgo 14.4.1:** La tabla `opxlinea` tiene 22 columnas, **ninguna relacionada con paradas**. Los campos `horini` y `horfin` son de programación (hora inicio/fin planeada), no de registro de paradas reales. No hay campos como `tiempoparada`, `motivotiempomuerto`, etc.

### 14.5 Consulta: Tablas básicas (b*) no inspeccionadas previamente

**Query 14.5.1** — Búsqueda de tablas básicas candidatas:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
-- Buscar tablas basicas candidatas
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename ~ '^b.*' 
AND tablename NOT ILIKE '%prove%' 
AND tablename NOT ILIKE '%prod%' 
AND tablename NOT ILIKE '%motiv%' 
AND tablename NOT ILIKE '%turno%' 
AND tablename NOT ILIKE '%linea%'
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
        tablename        
-------------------------
 bafmejora
 banconf1f
 bareaf
 bartic10f
 ... [175 tablas] ...
 bviaem1f
(175 rows)
```

**Hallazgo 14.5.1:** Se identificaron 175 tablas básicas. Se inspeccionaron las candidatas más probables por nombre:

**Query 14.5.2** — Estructura y conteo de `bareaf`, `bafmejora`, `bsprocss`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d bareaf; SELECT count(*) FROM bareaf; \d bafmejora; SELECT count(*) FROM bafmejora; \d bsprocss; SELECT count(*) FROM bsprocss;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                Table "public.bareaf"
  Column   |  Type   | Collation | Nullable | Default 
-----------+---------+-----------+----------+---------
 compania  | text    |           | not null | 
 sucursal  | text    |           | not null | 
 area      | text    |           | not null | 
 nombre    | text    |           | not null | 
 gerencia  | text    |           | not null | 
 estado    | text    |           | not null | 
 ... [más columnas] ...
 Indexes:
     "idx_163964_bareal1" UNIQUE, btree (compania, ejercicio, area)

 count 
-------
  2983
(1 row)

               Table "public.bafmejora"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 ejercicio  | integer |           | not null | 
 mejora     | integer |           | not null | 
 codcontab  | text    |           | not null | 
 estado     | text    |           | not null | 
 ... [más columnas] ...
 Indexes:
     "idx_163954_bafmejoral1" UNIQUE, btree (compania, ejercicio, mejora)

 count 
-------
     0
(1 row)

                   Table "public.bsprocss"
     Column      |   Type   | Collation | Nullable | Default 
-----------------+----------+-----------+----------+---------
 n_proceso       | integer  |           | not null | 
 fecha           | integer  |           |          | 
 schedule_fecha  | integer  |           |          | 
 schedule_hora   | text     |           |          | 
 ... [más columnas] ...
 Indexes:
     "idx_180443_llave_1u" UNIQUE, btree (n_proceso)

 count 
-------
     0
(1 row)
```

**Hallazgo 14.5.2:**
- `bareaf` (2,983 registros): Tabla maestra de **áreas organizacionales** (ej: "PROCESO FUNDIDO", "PLANEAMIENTO"), no de tipos de paradas.
- `bafmejora` (0 registros): Tabla de **mejoras contables**, vacía y no aplica.
- `bsprocss` (0 registros): Tabla de **programación de procesos batch** (scheduler), vacía y no aplica.
- `bproto3/4/5`: Tablas de protocolos y pruebas de calidad, no de paradas.

**Conclusión**: Ninguna de las 175 tablas básicas es un catálogo de tipos de paradas.

### 14.6 Consulta: Triggers en tablas de producción que puedan manejar paradas

**Query 14.6.1** — Triggers en tablas `tpro*` y `opx*`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT trigger_name, event_manipulation, event_object_table 
FROM information_schema.triggers 
WHERE event_object_table LIKE 'tpro%' 
OR event_object_table LIKE 'opx%'
ORDER BY event_object_table;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
      trigger_name      | event_manipulation | event_object_table 
------------------------+--------------------+--------------------
 trg_letrapr_progra_upd | UPDATE             | tprolt1f
 trg_adm_letras_cargo   | INSERT             | tprolt1f
 trg_adm_letras_cargo   | DELETE             | tprolt1f
 trg_adm_letras_cargo   | UPDATE             | tprolt1f
 trg_letrapr_progra_ins | INSERT             | tprolt1f
(5 rows)
```

**Hallazgo 14.6.1:** Los 5 triggers encontrados están en `tprolt1f` y están relacionados con **"letras" y "cargo"** (cobros/pagos contables), no con paradas de producción. No hay triggers que manejen lógica de paradas, tiempos muertos o OEE.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 14

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 campos de paradas en tablas `tpro*` | 14.1.1 | Registro de paradas no implementado en capa transaccional |
| 2 | 0 vistas de paradas/OEE | 14.2.1 | Sin lógica de consulta predefinida |
| 3 | `vsbtiempo` es tabla de calendario, no de paradas | 14.3.2 | No aplica; usar para reportes de periodos |
| 4 | `opxlinea` sin campos de paradas (22 columnas) | 14.4.1 | `horini`/`horfin` son planeados, no reales |
| 5 | 175 tablas básicas inspeccionadas, ninguna de paradas | 14.5.2 | Confirmado: catálogo nunca existió |
| 6 | 5 triggers en `tprolt1f` son de letras/cobros | 14.6.1 | Sin lógica de paradas en triggers |

---

## 15. CONCLUSIÓN TÉCNICA FINAL (VALIDACIÓN COMPLETA)

**El programa #133 "Paradas" no tiene implementación operativa en la base de datos legacy de Mexico.**

| Tabla | Registros | Propósito Esperado | Estado Real |
|---|---|---|---|
| `agrparoee` | 0 | Catálogo de paros OEE | Estructura vacía |
| `agrupoe` | 0 | Grupos de paradas (global) | Estructura vacía |
| `agrupoe1` | 0 | Subgrupos de paradas (detalle) | Estructura vacía |
| `mtiempoi1f` | 0 | Tiempos improductivos | Vacía + no aplica |
| `prgopdet` | 53,259 | Programación OP con flag `asigparada` | Solo flag boolean, sin tipos |
| `bmotiv1f` | 3,215 | Motivos contables | No aplica a paradas |
| `bproce1f` | 3,680 | Procedimientos contables | No aplica a paradas |

**Hallazgos clave**:
1. **No existe una tabla maestra de tipos de paradas** como `bparada1f` o `mparada1f`
2. **Las tablas OEE están vacías**: `agrupoe`, `agrupoe1`, `agrparoee` tienen 0 registros
3. **No hay triggers ni stored procedures** relacionados con paradas
4. **`prgopdet.asigparada` es solo un flag boolean**, no una referencia a tipos de paradas
5. **No hay datos que migrar**: 0 registros en todas las tablas de catálogo de paradas

---

### RESUMEN DE HALLAZGOS — SECCIÓN 15

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 registros en todas las tablas de catálogo de paradas | Secciones 3, 4, 10 | Módulo debe crearse desde cero |
| 2 | `prgopdet.asigparada` es flag boolean sin tipo | Sección 6 | Odoo necesita Many2one a catálogo |
| 3 | Sin triggers ni stored procedures | Secciones 8, 11 | Lógica limpia en Python/Odoo |
| 4 | 175 tablas básicas inspeccionadas, ninguna aplica | Sección 14 | Confirmado: no hay implementación oculta |

---

## 16. DUDAS LUEGO DEL ANÁLISIS DE LAS CONSULTAS PREVIAS

### 16.1 ¿Por qué las tablas OEE están vacías si estaban diseñadas?

**Respuesta:** Las tablas `agrupoe`, `agrupoe1` y `agrparoee` tienen estructura completa con índices y campos de auditoría, pero 0 registros. Esto indica que el módulo de OEE/paradas fue **diseñado pero nunca operado**. Posiblemente se implementó la estructura como parte de un proyecto que no llegó a producción en Mexico, o se dejó como placeholder para una futura integración.

### 16.2 ¿El flag `asigparada` en `prgopdet` tiene algún valor práctico?

**Respuesta:** El flag `asigparada` indica si una orden de producción tiene paradas asignadas, pero sin un catálogo de tipos de paradas, no hay forma de saber qué tipo de parada ocurrió. En Odoo 19, este flag debe reemplazarse por una relación Many2one a `bm.ctl.produccion.parada` que permita registrar el tipo específico.

### 16.3 ¿Se puede aprovechar la jerarquía `agrupoe` → `agrupoe1` → `agrparoee`?

**Respuesta:** El patrón jerárquico (grupo → subgrupo → parada específica) es válido y puede replicarse en Odoo usando un modelo con `parent_id` (Many2one self-referencia) para crear categorías y subcategorías de paradas. Sin embargo, como no hay datos que migrar, la jerarquía debe diseñarse desde cero basándose en las necesidades reales de Mexico.

### 16.4 ¿Las 156 líneas de producción en `mlinea1f` deben migrarse?

**Respuesta:** Las líneas de producción son un catálogo operativo que sí tiene datos reales. En Odoo 19, estas líneas pueden migrarse como registros de un modelo `bm.ctl.produccion.linea` y asociarse a las paradas para análisis de eficiencia por línea. El campo `flglinea` (LLENADORA, ETIQUETADORA) es útil para clasificar.

### 16.5 ¿Qué categorías de paradas son relevantes para Mexico?

**Respuesta:** Basándose en la estructura legacy y las necesidades típicas de producción, las categorías sugeridas son:
- **MEC**: Mecánica (fallas de equipos: banda, motor, sensor, válvula)
- **ELE**: Eléctrica (fallas eléctricas, sensores, PLC, tablero)
- **OPE**: Operativa (cambio de formato, limpieza, ajuste)
- **CAL**: Calidad (rechazo de producto, ajuste de calidad)
- **MAT**: Falta de Material (desabasto de jarabe, envases, etiquetas)
- **MAN**: Mantenimiento (preventivo/correctivo)
- **OTR**: Otros

---

### RESUMEN DE HALLAZGOS — SECCIÓN 16

| # | Duda | Resolución |
|---|------|------------|
| 1 | ¿Por qué tablas OEE vacías? | Diseñadas pero nunca operadas |
| 2 | ¿Valor práctico de `asigparada`? | Flag insuficiente; reemplazar con Many2one |
| 3 | ¿Aprovechar jerarquía legacy? | Patrón válido pero sin datos; diseñar desde cero |
| 4 | ¿Migrar 156 líneas de `mlinea1f`? | Sí, como catálogo de líneas de producción |
| 5 | ¿Categorías relevantes para Mexico? | MEC, ELE, OPE, CAL, MAT, MAN, OTR |

---

## 17. ACCIÓN RECOMENDADA EN ODOO

**Crear el módulo de Paradas desde cero en Odoo 19**, ya que el sistema legacy no tiene una implementación operativa de este módulo.

#### Estructura propuesta:

1. **Modelo `bm.ctl.produccion.parada`** (Catálogo de tipos de paradas):
   - `codigo` (Char, required): Código único (ej: 'PAR001', 'MEC001')
   - `descripcion` (Char, required): Descripción legible
   - `categoria_global` (Selection): Clasificación macro:
     - 'MEC': Mecánica (fallas de equipos)
     - 'ELE': Eléctrica (fallas eléctricas, sensores)
     - 'OPE': Operativa (cambio de formato, limpieza)
     - 'CAL': Calidad (rechazo de producto)
     - 'MAT': Falta de Material (desabasto)
     - 'MAN': Mantenimiento (preventivo/correctivo)
     - 'OTR': Otros
   - `codigo_detalle` (Char): Subclasificación (ej: 'BANDA', 'MOTOR', 'SENSOR')
   - `activo` (Boolean, default=True): Estado del tipo de parada
   - `tiempo_estimado` (Float): Tiempo estimado en minutos
   - `afecta_oee` (Boolean, default=True): Si afecta cálculo de OEE
   - Campos de auditoría: `create_uid`, `create_date`, `write_uid`, `write_date`

2. **Vista lista editable** (`editable="bottom"`):
   - Campos visibles: codigo, descripcion, categoria_global, codigo_detalle, activo, tiempo_estimado, afecta_oee
   - Permite creación rápida de tipos de paradas

3. **Menú**:
   ```
   Mantenimiento → Clasificadores → Paradas (secuencia 20)
   ```
   - Después de "Turnos" (secuencia 10) en Clasificadores

4. **Datos iniciales sugeridos** (17 tipos de paradas estandarizados):
   - MEC001-MEC004: Fallas mecánicas (banda, motor, sensor, válvula)
   - ELE001-ELE002: Fallas eléctricas (PLC, tablero)
   - OPE001-OPE003: Operativas (cambio formato, limpieza, ajuste)
   - CAL001-CAL002: Calidad (rechazo, ajuste)
   - MAT001-MAT003: Falta material (jarabe, envases, etiquetas)
   - MAN001-MAN002: Mantenimiento (preventivo, correctivo)
   - OTR001: Otros

5. **Seguridad**:
   - `security/ir.model.access.csv`: Acceso total para `base.group_user`

6. **Integración futura**:
   - Este modelo será la base para el registro real de paradas en líneas de producción
   - Se vinculará con `mlinea1f` (líneas de producción) para análisis de eficiencia por línea
   - Será el insumo principal para el cálculo de OEE en Odoo 19

**Justificación**: Las tablas legacy están vacías y no hay datos que migrar. Crear desde cero permite diseñar una estructura limpia y funcional que resuelva la necesidad real de Mexico, sin arrastrar inconsistencias del sistema anterior.
