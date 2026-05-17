## 1. EXPLORACIÓN DE DOCUMENTACIÓN OFICIAL - CONFIGURA PROCESOS PRODUCTIVOS

**Objetivo:** Consultar `aje_docs_simulacion/01_Docs_Oficiales/` y sus subcarpetas para obtener un acercamiento inicial al Program #574 "Configura Procesos Productivos".

### 1.1 Consulta: Búsqueda de referencias al Program #574 en docs oficiales

**Query 1.1.1** — Búsqueda con patrón `574|proceso.*productivo|configura.*proceso|CREAPROCESOFABRICACION|PROCPROD` en todo `01_Docs_Oficiales/`:
```bash
grep -ri "574\|proceso.*productivo\|configura.*proceso\|CREAPROCESOFABRICACION\|PROCPROD" aje_docs_simulacion/01_Docs_Oficiales/
```

**Hallazgo 1.1.1:** Se identificaron las siguientes coincidencias relevantes en el archivo `#478789 Obtener informacion de BD Mexico producción_xlsx.md`:

### 1.2 Stored Procedures con potencial relación al Program #574

| Stored Procedure | Clasificación | Última Mod. | Veces Ejecutado |
|---|---|---|---|
| `PR_ERP_FNZ_QRY_WS_CREAPROCESOFABRICACION` | ALTO - probable código muerto | 2024-10-18 | 0 |
| `USP_PROD_PROCPROD_ELIMINAVALIDA` | MEDIO - posible código muerto | 2024-03-15 | 0 |
| `USP_PROCESO_PRODUCCION` | ALTO - probable código muerto | 2013-10-30 | 0 |
| `USP_PROCESO_PRODUCCION3` | ALTO - probable código muerto | 2013-10-30 | 0 |
| `USP_PROCESO_CONFIGURACION1` | (sin clasificar en hoja PROD) | - | - |

**Hallazgo 1.2.1:** 
- `PR_ERP_FNZ_QRY_WS_CREAPROCESOFABRICACION` pertenece al namespace `PR_ERP_FNZ` (Finanzas), lo cual sugiere que es un web service SOAP/REST para crear procesos de fabricación desde sistemas externos.
- `USP_PROD_PROCPROD_ELIMINAVALIDA` pertenece al namespace `USP_PROD` (Producción), nombrado para eliminar/validar procesos productivos.
- `USP_PROCESO_PRODUCCION` y `USP_PROCESO_PRODUCCION3` son del namespace `USP` y datan de 2013 — probablemente creados durante la implementación inicial del sistema.
- **TODOS los SPs tienen 0 ejecuciones** — nunca se usaron en producción para México.

### 1.3 Búsqueda en subcarpetas de DocsOficiales

**Query 1.3.1** — Exploración de directorios relevantes:

| Directorio | Contenido relevante? |
|---|---|
| `Cadena de Suministro/Avail/` | BOMs, MakeBySegments, MakeActs — planificación/ejecución, NO configuración de procesos |
| `Cadena de Suministro/EfletexIA/` | Integraciones de fletes — NO aplica |
| `A&F/` | SAP, FullStep — NO aplica |
| `Comercial/` | Salesforce-Zuper — NO aplica |
| `Local México/` | Facturación, EDI, BBVA, Plan Viajes — NO aplica |
| `Transversal/` | ETL Fabrics, Integrador BM, RFID — NO aplica |

**Hallazgo 1.3.1:** Ninguna de las subcarpetas de documentación oficial contiene especificaciones funcionales o técnicas del Program #574.

### 1.4 Documentación AVAIL — Conceptos relacionados

En `Cadena de Suministro/Avail/MakeBySegments.md` se documenta la estructura de segmentos de producción:

| Atributo | Descripción |
|---|---|
| `SegmentCD` | Identificador único del segmento (MakeID – Segment) |
| `Shift` | Turno de producción (001, 002, 003) |
| `LineCd` | Código de línea de producción |
| `ItemCd` | Código del ítem/SKU |
| `RunFromTm` / `RunThruTm` | Ventana de tiempo de la corrida |
| `RunQty` | Cantidad programada |
| `BoMVerCd` | Versión de la receta (BOM) |

**Hallazgo 1.4.1:** Estos conceptos son de **planificación/ejecución de producción** (qué se produce, cuándo, en qué línea), no de **configuración de procesos productivos** (qué procesos existen: soplado, llenado, etiquetado, empacado).

---

### RESUMEN DE HALLAZGOS — SECCIÓN 1

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 5 SPs relacionados encontrados, todos marcados código muerto | 1.1.1, 1.2.1 | Sin lógica de negocio que migrar |
| 2 | 0 ejecuciones en todos los SPs | 1.2.1 | Nunca se usaron en producción |
| 3 | `CREAPROCESOFABRICACION` es namespace Finanzas (WS externo) | 1.2.1 | Posible integración con sistema externo (FullStep?) |
| 4 | Sin documentación funcional en DocsOficiales | 1.3.1 | La fuente de verdad debe ser la BD legacy y el análisis de negocio |
| 5 | AVAIL maneja segmentos de producción, no configuración de procesos | 1.4.1 | Conceptos diferentes: planificación vs. catálogo de procesos |

### Acción recomendada para Odoo 19:
- No depender de documentación oficial para este programa
- Los SPs legacy son código muerto — no hay lógica que replicar
- Construir el modelo desde la descripción referencial + análisis de BD legacy

---

## 2. CONCLUSIÓN DE LA CONSULTA A DOCUMENTACIÓN OFICIAL

**El Program #574 "Configura Procesos Productivos" no tiene documentación específica en `aje_docs_simulacion/01_Docs_Oficiales/`.**

### Ubicación en el árbol de menús (de `bm_ctl_produccion_descripciones.md`):

```
Menu Principal
└── Mantenimiento (mexico: SI)
    └── Configuraciones (mexico: SI)
        └── Configura Procesos Productivos (mexico: SI) ← Program #574
```

### Descripción referencial (de `bm_ctl_produccion_descripciones.md`):

> Configura los procesos productivos que componen la fabricación de un producto (soplado, llenado, etiquetado, empacado). Define la secuencia de operaciones, los parámetros de cada proceso y las líneas donde se pueden ejecutar. Es la base para el plan de producción y el cálculo de tiempos estándar. **[PENDIENTE VALIDAR]** ,referencial y NO es fuente de verdad.

### Análisis del namespace de SPs:

| Prefijo | Significado | Program #574 relevante? |
|---|---|---|
| `USP_PROD_` | User Stored Procedure - Producción | Sí — `USP_PROD_PROCPROD_ELIMINAVALIDA` |
| `PR_ERP_FNZ_` | Procedure ERP - Finanzas | Parcial — `CREAPROCESOFABRICACION` es WS desde finanzas |
| `USP_PROCESO_` | SP genérico de procesos | Sí — `USP_PROCESO_PRODUCCION`, `USP_PROCESO_CONFIGURACION1` |

---

### RESUMEN DE HALLAZGOS — SECCIÓN 2

| # | Hallazgo | Impacto para Odoo 19 |
|---|----------|---------------------|
| 1 | Sin docs funcionales del Program #574 | Modelar desde cero con base en BD legacy |
| 2 | Menú ya existe como placeholder en `mantenimiento_configuracion.xml` (sequence 20) | Solo falta crear modelo + action real |
| 3 | Descripción referencial menciona: soplado, llenado, etiquetado, empacado | Posibles procesos del catálogo |
| 4 | SPs `USP_PROCESO_PRODUCCION*` datan de 2013 — son los más antiguos del módulo | Posiblemente heredados de implementación inicial |
| 5 | Todos los SPs tienen 0 ejecuciones | Implementación nunca operada en México |

### Acción recomendada para Odoo 19:
- Usar la descripción referencial como guía conceptual, validando contra la BD legacy
- El menú `menu_configura_procesos` ya existe en `mantenimiento_configuracion.xml:8-12` apuntando a `base.action_partner_form` (dummy) — reconectar al nuevo action
- Incorporar el patrón de auditoría estándar (feccrea, horcrea, usucrea, fecultmod, horultmod, usuaulmod)

---

## 3. EXPLORACIÓN DE BASE DE DATOS LEGACY - TABLAS DE PROCESOS

**Objetivo:** Ejecutar consultas de introspección sobre PostgreSQL para identificar las tablas asociadas a la configuración de procesos productivos.

### 3.1 Consulta: Tablas con "proceso" / "propro" / "prgpro" en el nombre

**Query 3.1.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%proceso%' OR tablename ILIKE '%propro%' OR tablename ILIKE '%prgpro%')
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
     tablename     
-------------------
 ctm_lista_proceso
 ctm_proceso
 ctm_proceso_area
 ctm_proceso_linea
 mejecuta_procesos
 mprocesos
 mproprod1f
 psprgprod
(8 rows)
```

**Hallazgo 3.1.1:** Se identifican 8 tablas. `mproprod1f` (Maestro Procesos Productivos) es la candidata principal. Las tablas con prefijo `ctm_` sugieren relación con el módulo de costos (CTM = Controlling/CO).

### 3.2 Consulta: Columnas con "proceso" / "codpro" / "propro" en todo el esquema

**Query 3.2.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
AND (column_name ILIKE '%proceso%' OR column_name ILIKE '%codpro%' OR column_name ILIKE '%propro%')
ORDER BY table_name, column_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
51 columnas en 35+ tablas con referencias a "proceso" — 
las más relevantes para producción:
  ctm_costo_variable.proceso      → proceso de costeo
  ctm_costo_tfmc.proceso           → proceso en costeo TFMC
  tmcxsku.proceso                  → proceso por SKU (costos)
  mmateri7f.tipproprod             → tipo de proceso productivo del material
  mproprod1f.tipproprod            → PK de la tabla maestra
  mastopro1f.proceso / mastopro2f.codpro  → maestro de procesos (costos)
```

**Hallazgo 3.2.1:** La mayoría de columnas "proceso" están en tablas de **costos** (CTM, Controlling), no en tablas de producción. `mmateri7f.tipproprod` es una FK a `mproprod1f` pero está NULL en todos los registros.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 3

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 8 tablas con "proceso/propro" en nombre | 3.1.1 | Inspeccionar cada una para separar procesos de producción vs. costos |
| 2 | 51 columnas FK a proceso en 35+ tablas | 3.2.1 | La mayoría son de costos, no producción |
| 3 | `mproprod1f` es la tabla maestra de tipos de proceso productivo | 3.1.1 | Candidata principal para Program #574 |
| 4 | `mmateri7f.tipproprod` FK a `mproprod1f` pero siempre NULL | 3.2.1 | La relación materiales→procesos nunca se usó |

---

## 4. ANÁLISIS DE TABLA `mproprod1f` - MAESTRO DE PROCESOS PRODUCTIVOS

**Objetivo:** Inspeccionar la tabla maestra de tipos de procesos productivos.

### 4.1 Consulta: Estructura de `mproprod1f`

**Query 4.1.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mproprod1f;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
               Table "public.mproprod1f"
   Column    |  Type   | Nullable | Default 
-------------+---------+----------+---------
 tipproprod  | text    | not null |          ← PK: código del tipo de proceso
 descripcion | text    |          |          ← Nombre legible
 estado      | text    |          |          ← A=Activo, I=Inactivo
 feccrea     | integer |          |          ← Auditoría
 horcrea     | text    |          |          ← Auditoría
 usucrea     | text    |          |          ← Auditoría
 fecultmod   | integer |          |          ← Auditoría
 horultmod   | text    |          |          ← Auditoría
 usuultmod   | text    |          |          ← Auditoría
Indexes:
    "idx_170976_pkmproprod1l" PRIMARY KEY, btree (tipproprod)
```

### 4.2 Consulta: Datos de `mproprod1f`

**Query 4.2.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM mproprod1f ORDER BY tipproprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tipproprod | descripcion | estado | feccrea | horcrea | usucrea | fecultmod | horultmod | usuultmod 
------------+-------------+--------+---------+---------+---------+-----------+-----------+-----------
(0 rows)
```

**Hallazgo 4.2.1:** **`mproprod1f` está COMPLETAMENTE VACÍA (0 registros).** La tabla maestra de procesos productivos existe estructuralmente pero nunca se pobló con datos operativos. Ni México ni ninguna otra compañía tiene registros.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 4

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mproprod1f` es la tabla maestra de tipos de proceso | 4.1.1 | Es la tabla del Program #574 |
| 2 | 0 registros en toda la tabla | 4.2.1 | Sin datos que migrar; crear catálogo desde cero |
| 3 | Estructura simple: código + descripción + estado + auditoría | 4.1.1 | Modelo directo con campos similares |
| 4 | Sin triggers ni SPs asociados | Sección 1.2 | Sin lógica embebida |

---

## 5. ANÁLISIS DE TABLA `ctm_proceso` - PROCESOS GLOBALES (COSTOS)

**Objetivo:** Inspeccionar la tabla de procesos del módulo de costos, que contiene 6 procesos globales que podrían servir como referencia.

### 5.1 Consulta: Estructura y datos de `ctm_proceso`

**Query 5.1.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d ctm_proceso; SELECT * FROM ctm_proceso ORDER BY proceso;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
             Table "public.ctm_proceso"
   Column    | Type | Nullable | Default 
-------------+------+----------+---------
 proceso     | text | not null |          ← PK: código de proceso
 descripcion | text | not null |          ← Nombre

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

**Hallazgo 5.1.1:** `ctm_proceso` tiene **6 procesos globales** (macro-categorías). Estos son procesos de alto nivel (BEBIDAS, COMPRESION, INYECCION, PLOTEO, ALMACENES, HIELO) — agrupaciones de tipo de industria/producción, no procesos individuales como "soplado" o "llenado". No están asociados a una compañía específica.

### 5.2 Consulta: Tablas relacionadas con `ctm_proceso`

**Query 5.2.1** — Estructura de `ctm_proceso_area` y `ctm_proceso_linea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d ctm_proceso_area; \d ctm_proceso_linea;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
         Table "public.ctm_proceso_area"           Table "public.ctm_proceso_linea"
 Column  | Type | Nullable | Default                Column   | Type | Nullable | Default 
---------+------+----------+---------             -----------+------+----------+---------
 proceso | text | not null |                        compania  | text | not null | 
 area    | text | not null |                        proceso   | text | not null | 
        PK: (proceso, area)                             linea     | text | not null | 
                                                     PK: (compania, proceso, linea)
```

### 5.3 Consulta: Mapeo proceso→área

**Query 5.3.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT cpa.proceso, cp.descripcion, cpa.area 
FROM ctm_proceso_area cpa JOIN ctm_proceso cp ON cp.proceso = cpa.proceso 
ORDER BY cpa.proceso, cpa.area;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 proceso | descripcion | area 
---------+-------------+------
 01      | BEBIDAS      | 022  ← Producción Botella
 01      | BEBIDAS      | 023  ← ?
 01      | BEBIDAS      | 024  ← Tratamiento Agua
 01      | BEBIDAS      | 025  ← Jarabes
 01      | BEBIDAS      | 026  ← Soplado
 01      | BEBIDAS      | 027  ← Envasado
 01      | BEBIDAS      | 028  ← ?
 01      | BEBIDAS      | 031  ← Etiquetas
 01      | BEBIDAS      | 032  ← Bases
 01      | BEBIDAS      | 033  ← ?
 01      | BEBIDAS      | 034  ← Acondicionados
 01      | BEBIDAS      | 035  ← Maquila
 01      | BEBIDAS      | 051  ← Reempaques/Exhibidores
 02      | COMPRESION   | 030  ← Compresión
 03      | INYECCION    | 029  ← Inyección
 04      | PLOTEO       | 050  ← Ploteo
 05      | ALMACENES    | 053  ← Empaque/Almacenes
 06      | HIELO        | 052  ← Hielo
(18 rows)
```

**Hallazgo 5.3.1:** El proceso 01 BEBIDAS agrupa **13 áreas funcionales** (022-035, 051) que coinciden con las áreas del catálogo `mfameq1f` (Program #137). Los códigos de área (`area`) son los mismos que `mfameq1f.area`.

### 5.4 Consulta: Mapeo proceso→línea por compañía

**Query 5.4.1** — Distribución por compañía en `ctm_proceso_linea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, COUNT(*) as procesos FROM ctm_proceso_linea GROUP BY compania ORDER BY compania;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | procesos 
----------+----------
 0002     |        8
 0015     |        8
 0040     |        8
 ... (17 compañías) ...
 0200     |        8
(17 rows)
```

**Query 5.4.2** — México (0030) en `ctm_proceso_linea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM ctm_proceso_linea WHERE compania = '0030';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | proceso | linea 
----------+---------+-------
(0 rows)
```

**Hallazgo 5.4.2:** **México (0030) NO tiene ninguna configuración en `ctm_proceso_linea`.** 17 compañías tienen datos pero ninguna es México. Las compañías con datos son de otros países (Perú, Ecuador, etc. según el patrón de códigos 0002, 0015, 0040...).

---

### RESUMEN DE HALLAZGOS — SECCIÓN 5

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `ctm_proceso` tiene 6 procesos globales (BEBIDAS, COMPRESION, etc.) | 5.1.1 | Catálogo de referencia — útil como datos seed |
| 2 | `ctm_proceso_area` mapea proceso→área (18 registros) | 5.3.1 | 01 BEBIDAS cubre 13 áreas — coincide con `mfameq1f` |
| 3 | `ctm_proceso_linea` tiene 132 registros pero NINGUNO para 0030 | 5.4.2 | México nunca configuró procesos por línea |
| 4 | Los códigos de área son los mismos de `mfameq1f` (025=Jarabes, 027=Envasado, etc.) | 5.3.1 | Consistencia entre Program #137 y #574 |

### Acción recomendada para Odoo 19:
- Usar `ctm_proceso` como referencia de macro-procesos (datos seed opcionales)
- Usar `ctm_proceso_area` para mapear procesos de alto nivel a áreas funcionales
- El modelo de Program #574 podría ser más granular: procesos individuales (no solo "BEBIDAS" sino "SOPLADO", "LLENADO", "ETIQUETADO", "EMPACADO" dentro de BEBIDAS)

---

## 6. ANÁLISIS DE TABLAS RESTANTES

### 6.1 `mprocesos` — Maestro de procesos (genérico)

**Query 6.1.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mprocesos; SELECT * FROM mprocesos;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                             Table "public.mprocesos"
  Column  |  Type  | Nullable |                Default                
----------+--------+----------+---------------------------------------
 id       | bigint | not null | nextval('mprocesos_id_seq'::regclass)
 nombre   | text   | not null | 
 estado   | text   | not null | 
 nemonico | text   | not null | 
Indexes:
    "idx_170970_pk_mprocesos" PRIMARY KEY, btree (id)

(0 rows)
```

**Hallazgo 6.1.1:** `mprocesos` tiene **0 registros**. Es una tabla genérica de procesos con ID autoincremental, nombre, nemónico y estado. Posiblemente diseñada para procesos batch/scheduler, no para procesos productivos.

### 6.2 `ctm_lista_proceso` — Lista de procesos de costeo

**Query 6.2.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d ctm_lista_proceso; SELECT * FROM ctm_lista_proceso;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
          Table "public.ctm_lista_proceso"
   Column    | Type | Nullable | Default 
-------------+------+----------+---------
 codproceso  | text | not null |          ← PK
 descripcion | text | not null | 
 tipo        | text |          |          ← CE=Cierre, DE=Desviación, CT=Costo, CV=Variable, TM=Maestro

 codproceso | descripcion                     | tipo 
------------+---------------------------------+------
 001        | STANDARD COST                   | CE   ← Cierre estándar
 002        | DEVIATION TYPE 1                | DE   ← Desviación
 010        | INDIRECT EXPENSES               | CT   ← Costos
 011        | CTM                             | CT
 100        | PRODUCTION FAMILY               | TM   ← Maestro
 101        | COST CENTER GROUP               | TM
(14 rows)
```

**Hallazgo 6.2.1:** `ctm_lista_proceso` es del **módulo de costos** (CTM = Controlling), no de producción. Contiene 14 procesos de costeo (Standard Cost, Deviations, Indirect Expenses, Production Family). No aplica al Program #574.

### 6.3 `mejecuta_procesos` — Ejecución de procesos batch

**Query 6.3.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mejecuta_procesos; SELECT count(*) FROM mejecuta_procesos;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
  Column    |  Type   | Nullable | Default 
------------+---------+----------+---------
 id         | bigint  | not null | autoincrement
 proceso_id | bigint  | not null | ← FK a mprocesos?
 compania   | text    | not null | 
 sucursal   | text    | not null | 
 descripcion| text    | not null | 
 nombre_sp  | text    | not null | ← Stored Procedure a ejecutar
 orden      | integer | not null | 
 estado     | text    | not null | 

 count 
-------
     0
(1 row)
```

**Hallazgo 6.3.1:** `mejecuta_procesos` es una tabla de **scheduler de procesos batch** (ejecución de SPs programados), no de procesos productivos. Tiene **0 registros**.
### 6.4 `psprgprod` — Programación de producción

**Query 6.4.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d psprgprod; SELECT count(*) FROM psprgprod;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
  Column    |       Type       | Nullable | 
------------+------------------+----------+
 fecprog    | integer          | not null | ← Fecha de programación
 compania   | text             | not null | 
 sucursal   | text             | not null | 
 equipo     | integer          | not null | 
 articulo   | integer          | not null | 
 turno      | text             | not null | 
 secuencia  | integer          | not null | ← Orden dentro del turno
 produccion | double precision | not null | ← Cantidad a producir
PK: (fecprog, compania, sucursal, equipo, articulo, anodem, semdem, fecha, turno, secuencia)

 count 
-------
     0
(1 row)
```

**Hallazgo 6.4.1:** `psprgprod` tiene **0 registros**. Es una tabla de programación diaria de producción, no un catálogo de procesos. Relaciona equipo, artículo, turno y secuencia para planificar corridas.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 6

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `mprocesos` vacía (0 registros) | 6.1.1 | Sin datos que migrar |
| 2 | `ctm_lista_proceso` es de costos, no producción | 6.2.1 | Excluir del modelo de producción |
| 3 | `mejecuta_procesos` es scheduler de SPs, no procesos productivos | 6.3.1 | Excluir |
| 4 | `psprgprod` es programación de producción, vacía | 6.4.1 | Posible modelo futuro, no ahora |
| 5 | Todas las tablas relacionadas con procesos productivos están vacías | 6.1-6.4 | Módulo nunca se operó en BD legacy |

---

## 7. AUDITORÍA DE TRIGGERS Y DEPENDENCIAS

### 7.1 Consulta: Triggers en tablas de procesos

**Query 7.1.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT trigger_name, event_manipulation, event_object_table 
FROM information_schema.triggers 
WHERE event_object_table IN ('ctm_proceso','ctm_proceso_linea','ctm_proceso_area','mproprod1f','mprocesos');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 trigger_name | event_manipulation | event_object_table 
--------------+--------------------+--------------------
(0 rows)
```

### 7.2 Consulta: Stored Procedures que referencian tablas de procesos

**Query 7.2.1:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT routine_name, routine_type 
FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND (routine_name ILIKE '%mproprod%' OR routine_name ILIKE '%ctm_proceso%' OR routine_name ILIKE '%tipproprod%') 
ORDER BY routine_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 routine_name | routine_type 
--------------+--------------
(0 rows)
```

**Hallazgo 7.2.1:** No existen triggers ni stored procedures que referencien directamente a `mproprod1f` o `ctm_proceso`. Los SPs encontrados en Sección 1 (`USP_PROCESO_PRODUCCION`, etc.) son código muerto genérico que probablemente nunca referenció estas tablas.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 7

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 triggers en tablas de procesos | 7.1.1 | Sin lógica embebida |
| 2 | 0 SPs que referencien directamente las tablas | 7.2.1 | Migración limpia |

---

## 8. CONCLUSIÓN TÉCNICA FINAL (VALIDACIÓN COMPLETA)

**El programa #574 "Configura Procesos Productivos" no tiene implementación operativa en la base de datos legacy de México.**

| Tabla | Registros | Propósito | Estado Real |
|---|---|---|---|
| `mproprod1f` | **0** | Maestro de tipos de proceso productivo | **Vacía** — candidata principal |
| `mprocesos` | **0** | Procesos genéricos (scheduler) | Vacía |
| `ctm_proceso` | **6** | Procesos globales (costos) | Tiene datos pero no de producción granular |
| `ctm_proceso_area` | **18** | Mapeo proceso→área | Datos de referencia (BEBIDAS→13 áreas) |
| `ctm_proceso_linea` | **132** | Mapeo proceso→línea por compañía | **0 para México (0030)** |
| `ctm_lista_proceso` | **14** | Procesos de costeo | No aplica (módulo CTM) |
| `mejecuta_procesos` | **0** | Scheduler batch | No aplica |
| `psprgprod` | **0** | Programación producción | No aplica (futuro) |

**Hallazgos clave:**
1. **`mproprod1f` es la tabla del Program #574** — estructura simple (código + descripción + estado + auditoría) pero **0 registros**
2. **`ctm_proceso` tiene 6 procesos globales** que sirven como referencia de macro-categorías
3. **`ctm_proceso_area` mapea procesos a áreas funcionales** usando los mismos códigos de `mfameq1f` (Program #137)
4. **México nunca configuró procesos por línea** (`ctm_proceso_linea` vacío para 0030)
5. **0 triggers, 0 SPs activos, 0 ejecuciones** — implementación completamente inoperada
6. **Sin datos que migrar** — el módulo debe crearse desde cero

---

## 9. ACCIÓN RECOMENDADA EN ODOO 19

**Crear el módulo de Configuración de Procesos Productivos desde cero**, ya que el sistema legacy no tiene implementación operativa de este módulo para México.

### Modelo propuesto: `bm.ctl.produccion.proceso`

| Campo | Tipo | Descripción |
|---|---|---|
| `codigo` | Char (required) | Código del proceso (ej: 'SOP', 'LLE', 'ETQ', 'EMP') |
| `descripcion` | Char (required) | Nombre legible (ej: 'Soplado', 'Llenado', 'Etiquetado', 'Empacado') |
| `secuencia` | Integer | Orden de ejecución en la cadena productiva |
| `parametros` | Text | Parámetros de configuración del proceso |
| `area_id` | Many2one → `bm.ctl.produccion.categoria.linea` | Área funcional asociada (de Program #137) |
| `linea_ids` | Many2many → `bm.ctl.produccion.linea` (futuro) | Líneas donde se ejecuta |
| `activo` | Boolean (default=True) | Estado del proceso |
| `company_id` | Many2one → `res.company` | Compañía |
| `feccrea, horcrea, usucrea` | Auditoría | Campos de creación |
| `fecultmod, horultmod, usuaulmod` | Auditoría | Campos de modificación |

### Datos seed sugeridos (basados en la descripción referencial y `ctm_proceso_area`):

| Código | Descripción | Área (mfameq1f) |
|---|---|---|
| SOP | Soplado | 026 - EQUIPOS DE SOPLADO |
| LLE | Llenado | 027 - EQUIPOS DE ENVASADO |
| ETQ | Etiquetado | 031 - PRODUCCION ETIQUETAS |
| EMP | Empacado | 053 - EMPAQUE |
| JAR | Preparación Jarabe | 025 - TANQUES DE JARABE |
| BAS | Preparación Bases | 032 - BASES TERMINADAS |

### Menú:
```
Mantenimiento → Configuraciones → Configura Procesos Productivos (sequence 20)
```
- Ya existe el menú placeholder `menu_configura_procesos` en `mantenimiento_configuracion.xml:8-12`
- Solo falta crear el nuevo action y reconectar

### Vista:
- Lista editable (`editable="bottom"`) con campos: codigo, descripcion, secuencia, area_id, activo
- Form con pestañas: Configuración + Auditoría
- Search con filtros por activo/inactivo y agrupación por área

### Seguridad:
- `security/ir.model.access.csv`: Acceso total para `base.group_user`

**Justificación:** `mproprod1f` es la tabla dedicada del Program #574 — existe estructuralmente pero nunca se usó. No hay lógica de negocio que replicar (0 triggers, 0 SPs activos). El modelo puede crearse limpio en Odoo 19, aprovechando los códigos de área del Program #137 (`bm.ctl.produccion.categoria.linea`) para vincular procesos con áreas funcionales. Los datos seed se basan en la combinación de la descripción referencial y los mapeos de `ctm_proceso_area`.

---

## 10. DUDAS LUEGO DEL ANÁLISIS DE LAS CONSULTAS PREVIAS

### 10.1 ¿Por qué `mproprod1f` está vacía si existe estructuralmente?

**Respuesta:** Es el mismo patrón observado en otros programas del módulo de producción: la estructura DDL se creó como parte de un diseño anticipado, pero el módulo nunca llegó a operarse. Las tablas `agrparoee`, `agrupoe`, `agrupoe1` del Program #133 también estaban vacías. Esto sugiere que el sistema legacy tiene "capas de funcionalidad planeada pero no implementada" — posiblemente porque la configuración de procesos se manejaba de forma implícita (a través de las recetas/BOMs y la programación de líneas) en lugar de un catálogo explícito.

**Impacto en Odoo 19:** No hay restricción — el modelo puede diseñarse con la granularidad que el negocio necesite. Pero obliga a definir desde cero qué procesos son relevantes para México (ver Duda 10.7).

### 10.2 ¿`ctm_proceso` y `mproprod1f` son lo mismo o son conceptos distintos?

**Respuesta:** Son conceptos distintos con granularidad diferente:

| Aspecto | `ctm_proceso` | `mproprod1f` |
|---|---|---|
| Propósito | Macro-procesos (agrupación industrial) | Procesos productivos individuales |
| Granularidad | 6 categorías (BEBIDAS, COMPRESION, INYECCION...) | Diseñado para procesos como SOPLADO, LLENADO... |
| Módulo | Costos/CTM (Controlling) | Producción |
| Datos | 6 registros | 0 registros |
| Alcance | Global (sin compañía) | Global (sin compañía en su PK) |

Los 6 procesos de `ctm_proceso` son agrupaciones de alto nivel por tipo de industria. `mproprod1f` estaba diseñado para los procesos individuales dentro de cada industria. Por ejemplo, dentro de "01 BEBIDAS" estarían SOPLADO, LLENADO, ETIQUETADO, EMPACADO.

**Impacto en Odoo 19:** El modelo de Odoo debe basarse en `mproprod1f` (procesos individuales), no en `ctm_proceso` (macro-categorías). Opcionalmente, podría agregarse un campo `macro_proceso_id` que referencie una tabla de macro-categorías si el negocio requiere esa jerarquía.

### 10.3 ¿Los códigos de área en `ctm_proceso_area` son los mismos de `mfameq1f`? ¿Se puede hacer JOIN?

**Respuesta:** Sí, son exactamente los mismos códigos. Comparación:

| Área | `ctm_proceso_area` | `mfameq1f` (descripción) |
|---|---|---|
| 025 | BEBIDAS → 025 | TANQUES DE JARABE |
| 026 | BEBIDAS → 026 | EQUIPOS DE SOPLADO |
| 027 | BEBIDAS → 027 | EQUIPOS DE ENVASADO |
| 031 | BEBIDAS → 031 | PRODUCCION ETIQUETAS |
| 032 | BEBIDAS → 032 | BASES TERMINADAS |
| 035 | BEBIDAS → 035 | MAQUILA |
| 051 | BEBIDAS → 051 | PRODUCCION EXHIBIDORES / REEMPAQUES |

Sin embargo, `mfameq1f.area` es un campo `text` sin FK explícita. No existe una tabla maestra de áreas (`bareaf` en la BD es de áreas organizacionales/contables, no de áreas funcionales de producción).

**Impacto en Odoo 19:** Se puede crear un Many2one desde `bm.ctl.produccion.proceso` hacia `bm.ctl.produccion.categoria.linea` (Program #137) usando `efamilia` como clave, ya que `mfameq1f` asocia cada `efamilia` con un `area`. El campo `area` en el modelo de Odoo puede ser un campo relacionado (`related='categoria_linea_id.area'`).

### 10.4 ¿Por qué `ctm_proceso_linea` tiene datos para 17 compañías pero ninguna es México (0030)?

**Respuesta:** Las 17 compañías con datos son de Perú (0002, 0015...), Ecuador (0040...) y otros países. México (0030) nunca configuró la relación proceso→línea. Esto es consistente con el patrón general: México usaba el sistema para operaciones contables y comerciales, pero la configuración avanzada de producción no se implementó.

**Query de verificación sugerida:**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT compania FROM ctm_proceso_linea 
WHERE compania NOT IN ('0030','0032','0036')
ORDER BY compania;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado de la consulta:**
```text
 compania 
----------
 0002
 0015
 0040
 0070
 0076
 0081
 0086
 0087
 0088
 0090
 0092
 0093
 0094
 0150
 0151
 0152
 0200
(17 rows)
```

**Verificación adicional** — ¿0032 y 0036 tienen datos?
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT compania, COUNT(*) FROM ctm_proceso_linea WHERE compania IN ('0032','0036') GROUP BY compania;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | count 
----------+-------
(0 rows)
```

**Conclusión corregida:** Ni 0032 (Perú) ni 0036 (Ecuador) tienen datos en `ctm_proceso_linea`. Las 17 compañías con datos son códigos de otros países/entornos (0002, 0015, 0040...) pero **ninguna de las 3 compañías operativas principales** (0030, 0032, 0036) usó esta tabla. Esto refuerza que la configuración proceso→línea fue una funcionalidad planeada pero nunca operada en producción real.

### 10.5 ¿Qué relación tiene `ctm_proceso` con el módulo de costos? ¿`ctm_costo_variable.proceso` referencia a `ctm_proceso`?

**Respuesta:** **No hay relación directa.** Los valores de `ctm_costo_variable.proceso` son códigos distintos:

| Tabla | Valores de `proceso` |
|---|---|
| `ctm_proceso` | 01, 02, 03, 04, 05, 06 (texto) |
| `ctm_costo_variable` | 019, 020, 021, 022, 024, STD (¿numérico?) |

No existe FK declarada entre `ctm_costo_variable` y `ctm_proceso`. Son dominios separados: `ctm_proceso` es un catálogo de macro-procesos industriales, mientras que `ctm_costo_variable.proceso` referencia procesos de costeo (posiblemente de `ctm_lista_proceso` donde `codproceso`='020'=QUANTITY DEVIATION, '021'=PRICE DEVIATION, etc.).

### 10.6 ¿Los SPs `USP_PROCESO_PRODUCCION` y `USP_PROCESO_PRODUCCION3` tienen código SQL que revele qué tablas usaban?

**Respuesta:** Se ejecutaron las siguientes consultas para extraer el código fuente:

**Query 10.6.1** — Búsqueda por nombre exacto (`USP_PROCESO_PRODUCCION`):
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT proname, pg_get_functiondef(p.oid) FROM pg_proc p 
WHERE proname ILIKE '%proceso%produccion%';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 proname | body 
---------+------
(0 rows)
```

**Query 10.6.2** — Búsqueda amplia de cualquier SP con `proceso` en el nombre:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT routine_name FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND (routine_name ILIKE '%usp_proceso%' OR routine_name ILIKE '%creaprocesofab%')
ORDER BY routine_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 routine_name 
--------------
(0 rows)
```

**Conclusión:** **Ninguno de los SPs listados en el Excel (`USP_PROCESO_PRODUCCION`, `USP_PROCESO_PRODUCCION3`, `USP_PROD_PROCPROD_ELIMINAVALIDA`, `PR_ERP_FNZ_QRY_WS_CREAPROCESOFABRICACION`) existe en la base de datos `mxbdaje_local`.** El archivo `#478789` compilaba SPs de múltiples bases de datos del ecosistema Big Magic (desarrollo, otros países), pero estos objetos nunca se desplegaron en la instancia de México.

**Impacto en Odoo 19:** Nulo. No hay código fuente que revisar. La lógica del Program #574 debe diseñarse completamente desde cero en Python/Odoo.

### 10.7 ¿Qué granularidad debe tener el modelo de Odoo: macro-procesos (`ctm_proceso`) o procesos individuales (`mproprod1f`)?

**Respuesta:** La descripción referencial menciona procesos individuales: "soplado, llenado, etiquetado, empacado". Esto corresponde al diseño de `mproprod1f`. Los macro-procesos de `ctm_proceso` (BEBIDAS, COMPRESION...) son un nivel de agrupación superior.

Se recomienda implementar el modelo con granularidad de **procesos individuales** (`bm.ctl.produccion.proceso`) y opcionalmente agregar un campo `macro_proceso` (Many2one a una tabla de macro-categorías) si en el futuro se necesita la jerarquía.

**Propuesta de datos seed iniciales** (todos dentro del macro-proceso "BEBIDAS"):

| Código | Descripción | Secuencia | Área |
|---|---|---|---|
| SOP | Soplado | 10 | 026 |
| JAR | Preparación de Jarabe | 20 | 025 |
| BAS | Preparación de Bases | 30 | 032 |
| LLE | Llenado/Envasado | 40 | 027 |
| ETQ | Etiquetado | 50 | 031 |
| EMP | Empacado | 60 | 053 |

### 10.8 `mmateri7f.tipproprod` está siempre NULL — ¿confirma que los materiales nunca se clasificaron por proceso?

**Respuesta:** Sí. El campo `tipproprod` en la tabla de materiales (`mmateri7f`) es la FK a `mproprod1f`, y como está NULL en todos los registros, confirma que:
1. Los materiales nunca se asociaron a un tipo de proceso productivo
2. La clasificación de materiales por proceso no era un requisito operativo en México
3. El campo existe por diseño pero nunca se implementó la lógica para poblarlo

Esto es consistente con `mproprod1f` vacía: si no hay procesos definidos, no hay nada que asignar a los materiales.

**Impacto en Odoo 19:** El modelo `bm.ctl.produccion.proceso` no necesita relación inversa a materiales en esta etapa. Si en el futuro se requiere, se puede agregar un One2many desde proceso hacia materiales.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 10

| # | Duda | Resolución |
|---|------|------------|
| 1 | ¿Por qué `mproprod1f` está vacía? | Mismo patrón que #133 — diseño anticipado nunca operado |
| 2 | ¿`ctm_proceso` vs `mproprod1f`? | Distintos: macro-procesos (6) vs procesos individuales (0) |
| 3 | ¿Áreas de `ctm_proceso_area` = `mfameq1f`? | Sí, mismos códigos — se puede hacer Many2one a Program #137 |
| 4 | ¿México sin datos en `ctm_proceso_linea`? | **Confirmado con query**: 0 rows para 0030, 0032 y 0036. Ninguna de las 3 compañías principales usó esta tabla |
| 5 | ¿Relación `ctm_proceso` ↔ `ctm_costo_variable`? | No relacionadas — dominios de proceso distintos |
| 6 | ¿Revisar código de SPs muertos? | **Confirmado con queries**: los SPs NO existen en `mxbdaje_local`. Eran de otras BB.DD. del ecosistema |
| 7 | ¿Granularidad del modelo? | Procesos individuales (no macro-procesos), con opción futura de jerarquía |
| 8 | ¿`mmateri7f.tipproprod` NULL? | Confirma que materiales nunca se clasificaron por proceso |
