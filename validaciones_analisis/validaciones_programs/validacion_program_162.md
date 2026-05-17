## 1. AUDITORÍA DE ESTRUCTURAS DE DATOS, NIVELES DE AUTORIZACIÓN Y TRAZABILIDAD DE FÓRMULAS

**Objetivo:** Entender cómo están organizadas las tablas de fórmulas y aprobaciones, qué campos manejan, y si existe un flujo de aprobación multinivel operativo (autorizado por varias personas) en la base de datos de Mexico.

### 1.1 Consulta: Estructura de las tablas principales

**Query 1.1.1** — Describir estructura de 8 tablas clave:
```sql
\d tformula_
\d tmp_aprob_ped
\d maprob1f
\d maprobniv
\d taprob1f
\d taprob2f
\d taprob3f
\d taprob4f

 Table "public.tformula_"
  Column  |       Type       | Collation | Nullable | Default 
----------+------------------+-----------+----------+---------
 compania | text             |           |          | 
 sucursal | text             |           |          | 

 
              Table "public.tmp_aprob_ped"
    Column    |  Type   | Collation | Nullable | Default 
--------------+---------+-----------+----------+---------
 compania     | text    |           |          | 
 sucursal     | text    |           |          | 
 emisor       | text    |           |          | 
 docupedido   | text    |           |          | 
...
  Table "public.maprob1f"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 nivel      | text    |           | not null | 
 descripniv | text    |           | not null | 
 estado     | text    |           | not null | 
 feccrea    | integer |           | not null | 
 horcrea    | text    |           | not null | 
 usucrea    | text    |           | not null | 
 fecultmod  | integer |           | not null | 
 horultimod | text    |           | not null | 
 ultusumod  | text    |           | not null | 
 orden      | integer |           |          | 
 nivaprob   | text    |           |          | 
Indexes:
    "idx_168066_maprob1l1" UNIQUE, btree (compania, nivel)
    "idx_168066_maprob1l2" btree (compania, descripniv)  

Table "public.maprobniv"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 modulo     | text    |           | not null | 
 opcion     | text    |           | not null | 
 transaccio | text    |           | not null | 
 nivel      | text    |           | not null | 
 estado     | text    |           | not null | 
 feccrea    | integer |           | not null | 
 horcrea    | text    |           | not null | 
 usucrea    | text    |           | not null | 
 fecultmod  | integer |           | not null | 
 horultmod  | text    |           | not null | 
 ultusumod  | text    |           | not null | 
 tipoaprob  | text    |           |          | 
Indexes:
    "idx_168200_maprobnil1" UNIQUE, btree (compania, modulo, opcion, transaccio, nivel)     

Table "public.taprob1f"
   Column   |   Type   | Collation | Nullable | Default 
------------+----------+-----------+----------+---------
 compania   | text     |           | not null | 
 sucursal   | text     |           | not null | 
 area       | text     |           | not null | 
 caja       | smallint |           | not null | 
 transaccio | text     |           | not null | 
 nroserie   | text     |           |          | 
 nrodoc     | text     |           | not null | 
 persona    | integer  |           | not null | 
 nivel      | text     |           | not null | 
 corrautori | smallint |           | not null | 
 empleautor | integer  |           | not null | 
 fecautoriz | integer  |           | not null |

Table "public.taprob2f"
   Column   |   Type   | Collation | Nullable | Default 
------------+----------+-----------+----------+---------
 compania   | text     |           | not null | 
 sucursal   | text     |           | not null | 
 transaccio | text     |           | not null | 
 nroserie   | text     |           |          | 
 nrodoc     | text     |           | not null | 
 persona    | integer  |           | not null | 
 orden      | smallint |           | not null | 
 descrip    | text     |           | not null | 
 actualiza  | integer  |           | not null | 
 estado     | text     |           | not null | 

 Table "public.taprob3f"
   Column   |       Type       | Collation | Nullable | Default 
------------+------------------+-----------+----------+---------
 compania   | text             |           | not null | 
 sucursal   | text             |           | not null | 
 area       | text             |           | not null | 
 caja       | smallint         |           | not null | 
 transaccio | text             |           | not null | 
 serie      | text             |           | not null | 
 nrodoc     | text             |           | not null | 
 proveedor  | integer          |           | not null | 
 fecha      | integer          |           | not null | 

Table "public.taprob4f"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 sucursal   | text    |           | not null | 
 transaccio | text    |           | not null | 
 nrodoc     | text    |           | not null | 
 tcompra    | integer |           | not null | 
 nivel      | integer |           | not null | 
 empleautor | integer |           | not null | 
 fecautoriz | integer |           | not null | 
 observac   | text    |           | not null | 
 estado     | text    |           | not null | 
```

**Hallazgo 1.1.1:** Se identificaron 3 familias de tablas:
- **Fórmulas:** `tformula_` (contiene `articulo`, `nrosecu`, `material`, `porcent`, `cantidad` — estructura típica de recetas con componentes secuenciales)
- **Configuración de niveles:** `maprob1f` (catálogo de niveles con `nivel` + `descripniv`, campo `orden` jerárquico y `nivaprob`) y `maprobniv` (asigna niveles a combinaciones de módulo, opción y transacción por compañía, con `tipoaprob`)
- **Trámites de aprobación:** `taprob1f` a `taprob4f` (registran aprobaciones con `empleautor`, `fecautoriz`, `horautoriz`, `observac`; `taprob2f` tiene detalle por `orden`; `taprob3f` incluye datos financieros como `proveedor`, `total`, `moneda`; `taprob4f` registra aprobación por `tcompra` y `nivel`)

---

### 1.2 Consulta: Datos reales de las tablas de fórmulas y aprobación

**Query 1.2.1** — Muestreo de datos de `tformula_`:
```sql
SELECT * FROM tformula_ LIMIT 10;

compania | sucursal | articulo |               desc_sku               | estado | tamlote | nrosecu | material | porcent | factconv  |  cantidad  
----------+----------+----------+--------------------------------------+--------+---------+---------+----------+---------+-----------+------------
 0002     | 29       |   500195 | BIG COLA PET NO RETORNABLE 3300 ML 6 | A      |     698 |       7 |   300677 |     100 | 3.0669803 | 2140.75225
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       1 |     1854 |     100 |  0.049896 |   97.02144
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       2 |     3242 |     100 |   5.07105 | 11683.6992
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       3 |    30462 |     100 |        12 |      27648
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       4 |    38153 |     100 |     0.024 |     55.296
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       5 |    41282 |     100 |        12 |      27648
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       6 |    41300 |     100 |        12 |      27648
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       7 |   300745 |     100 |  0.929387 | 2141.30765
 0002     | 29       |   500269 | BIG COLA PET NO RETORNABLE 3300 ML 4 | A      |    1047 |       1 |     1854 |     100 | 0.1097712 |   96.98361
 0002     | 29       |   500269 | BIG COLA PET NO RETORNABLE 3300 ML 4 | A      |    1047 |       2 |     3242 |     100 |   11.1563 | 11680.6461
(10 rows)

```

**Hallazgo 1.2.1:** `tformula_` contiene 5,087 registros activos (estado = 'A'). Cada registro representa un ingrediente dentro de una receta de producto. Ejemplo: el SKU "BIG COLA PET 500 ML 12" tiene 7 ingredientes (material) con sus cantidades y porcentajes. **Solo tiene un campo `estado` genérico** — no tiene campos como `aprobador`, `fecaprob`, `nivel`, etc.

**Query 1.2.2** — Muestreo de `tmp_aprob_ped` (pedidos pendientes de aprobación):
```sql
SELECT * FROM tmp_aprob_ped LIMIT 10;

 compania | sucursal | emisor | docupedido | nropedido | cliente | ordcompra |  usuario  | seleccionado 
----------+----------+--------+------------+-----------+---------+-----------+-----------+--------------
 0030     | 0001     | 02     | 300        |     38679 | 1748604 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38680 | 1748609 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38682 | 1748611 |           | TAROSALIA | \x46
 ...
```

**Hallazgo 1.2.2:** Contiene pedidos en cola de autorización con usuario asignado (ej: "TAROSALIA"). La columna `seleccionado` es de tipo `bytea` (bandera binaria). Esto confirma que existe un mecanismo de selección previa antes de la aprobación formal.

**Query 1.2.3** — Configuración de niveles por módulo/transacción (`maprobniv`):
```sql
SELECT * FROM maprobniv;


 compania | modulo | opcion | transaccio | nivel | estado | feccrea | horcrea | usucrea  | fecultmod | horultmod | ultusumod | tipoaprob 
----------+--------+--------+------------+-------+--------+---------+---------+----------+-----------+-----------+-----------+-----------
 0002     | COL    | LG040  | OCO        | A     | A      |  735800 | 235843  | AOLIVERA |    735800 | 235905    | AOLIVERA  | L
 1000     | COL    | LG040  | OCO        | A     | A      |  736990 | 141818  | SYSTEM   |    736990 | 141818    | SYSTEM    | L
 0002     | COL    | LG040  | OCO        | C     | A      |  735800 | 235915  | AOLIVERA |    735800 | 235926    | AOLIVERA  | I
 1000     | COL    | LG040  | OCO        | C     | A      |  736990 | 141818  | SYSTEM   |    736990 | 141818    | SYSTEM    | I
 0100     | COL    | LG040  | OCO        |       | A      |  737286 | 184402  | MMENDOZA |    737286 | 184404    | MMENDOZA  | 
 4000     | COL    | LG040  | OCO        | A     | A      |  737452 | 101220  | SYSTEM   |    737452 | 101220    | SYSTEM    | L
 4000     | COL    | LG040  | OCO        | C     | A      |  737452 | 101220  | SYSTEM   |    737452 | 101220    | SYSTEM    | I
 3000     | COL    | LG040  | OCO        | A     | A      |  737452 | 101351  | SYSTEM   |    737452 | 101351    | SYSTEM    | L ...
```

**Hallazgo 1.2.3:** La tabla muestra que para el módulo "COL" (Compras) y transacción "OCO" (Orden de Compra), existen **dos niveles de aprobación configurados**: nivel "A" (tipo L = Liberación) y nivel "C" (tipo I = Inicial). Cada compañía tiene su propia configuración. Algunas compañías (0100, 0035, 0033, 0060, 0032) tienen el campo `nivel` vacío, lo que indica que **no tienen aprobación multinivel activada**.

**Query 1.2.4** — Definición de nombres de niveles (`maprob1f`):
```sql
SELECT * FROM maprob1f LIMIT 10;

 
 compania | nivel |   descripniv   | estado | feccrea | horcrea | usucrea | fecultmod | horultimod | ultusumod | orden | nivaprob 
----------+-------+----------------+--------+---------+---------+---------+-----------+------------+-----------+-------+----------
 0032     | 01    | JEFATURA       | 1      |  734377 | 213440  | MVEGA   |    734377 | 213440     | MVEGA     |     0 | 
 0032     | 02    | GERENCIA       | 2      |  734377 | 213440  | MVEGA   |    734377 | 213440     | MVEGA     |     0 | 
 0032     | 03    | DIRECCION      | 3      |  734377 | 213441  | MVEGA   |    734377 | 213441     | MVEGA     |     0 | 
 0032     | A     | COMPRAS NV.1   | 1      |  734377 | 213441  | MVEGA   |    734377 | 213441     | MVEGA     |     0 | 
 0032     | B     | COMPRAS NV.2   | 2      |  734377 | 213442  | MVEGA   |    734377 | 213442     | MVEGA     |     0 | 
 0032     | C     | COMPRAS NV.3   | 3      |  734377 | 213442  | MVEGA   |    734377 | 213442     | MVEGA     |     0 | 
 0032     | E     | PRE-APROBACION | 1      |  734377 | 213442  | MVEGA   |    734377 | 213442     | MVEGA     |     0 | 
 0032     | F     | APROBACION DCO | 3      |  734377 | 213443  | MVEGA   |    734377 | 213443     | MVEGA     |     0 | 
 0032     | N1    | VISTO          | 1      |  734377 | 213443  | MVEGA   |    734377 | 213443     | MVEGA     |     0 | 
 0032     | N2    | APROBACION     | 2      |  734377 | 213444  | MVEGA   |    734377 | 213444     | MVEGA     |     0 | 
(10 rows)
```

**Hallazgo 1.2.4:** Los niveles tienen nombres jerárquicos reales. Para la compañía 0032 se encontraron:

| Nivel | Nombre |
|-------|--------|
| 01 | JEFATURA |
| 02 | GERENCIA |
| 03 | DIRECCION |
| A | COMPRAS NV.1 |
| B | COMPRAS NV.2 |
| C | COMPRAS NV.3 |
| E | PRE-APROBACION |
| F | APROBACION DCO |
| N1 | VISTO |
| N2 | APROBACION |

Esto confirma que **el sistema sí soporta aprobación multinivel con nombres de cargo**, no solo niveles numéricos.

**Resumen**

"Empezamos mirando la tabla de fórmulas(Qeury 1.2.1) y notamos que no tiene campos de aprobación(solo estado='A'). Entonces buscamos dónde sí se configura eso: encontramos una cola de pedidos (Query 1.2.2 tmp_aprob_ped,se ve un usuario ej TAROSALIA  y un flag seleccionado), una tabla que asigna niveles a transacciones ( Query 1.2.3 en maprobniv,cada transaccion tienen niveles A,B..), y un catálogo que da nombre a esos niveles (Query 1.2.4 donde maprob1f define 01=JEFATURA,02=GERENCIA,A=COMPRAS NV.1 ..). Las 4 queries juntas revelan que el sistema de aprobación existe pero está desacoplado de las fórmulas."

---

### 1.3 Consulta: Columnas relacionadas con aprobación en todo el esquema

**Query 1.3.1** — Buscar columnas con nombres de aprobación/estado/firma en las tablas auditadas:
```sql
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('tformula_', 'tmp_aprob_ped', 'maprob1f', 'maprobniv', 'taprob1f')
  AND (column_name LIKE '%aprob%' OR column_name LIKE '%estado%'
       OR column_name LIKE '%status%' OR column_name LIKE '%firma%')
ORDER BY table_name, ordinal_position;

 table_name | column_name | data_type 
------------+-------------+-----------
 maprob1f   | estado      | text
 maprob1f   | nivaprob    | text
 maprobniv  | estado      | text
 maprobniv  | tipoaprob   | text
 taprob1f   | estado      | text
 tformula_  | estado      | text
(6 rows)
```

**Hallazgo 1.3.1:** De las 6 columnas encontradas, **5 son el campo `estado` genérico** (text) presente en casi todas las tablas. Solo 2 columnas son específicas de aprobación:
- `maprob1f.nivaprob` — nivel de aprobación (texto)
- `maprobniv.tipoaprob` — tipo de aprobación (L=Libera, I=Inicial) (ver hallazgo 1.1.1)

**Conclusión clave:** `tformula_` **no tiene ningún campo propio de aprobación**. Solo tiene `estado` = 'A' (Activo). Esto significa que la aprobación de fórmulas no se registra directamente en esta tabla.

**resumen** (hace falta?)

---

### 1.4 Consulta: Triggers de base de datos

**Query 1.4.1** — Buscar triggers en tablas de fórmulas y aprobación:
```sql
SELECT trigger_name, event_manipulation, event_object_table, action_statement
FROM information_schema.triggers
WHERE event_object_table LIKE '%formula%' OR event_object_table LIKE '%aprob%';

trigger_name | event_manipulation | event_object_table | action_statement 
 --------------+--------------------+--------------------+------------------
 (0 rows)
```

**Hallazgo 1.4.1:** **0 triggers encontrados.** No existe automatización a nivel de base de datos para el flujo de aprobación. Toda la lógica (quién aprueba, cuándo, qué pasa después) está programada en la capa de aplicación (Big Magic ERP), no en PostgreSQL.

**Conclusión para Odoo 19:** Al migrar, debemos implementar toda la lógica de aprobación en Python/Odoo — no podemos depender de triggers ni procedimientos almacenados en la base de datos.

---

### 1.5 Consulta: Tablas complementarias (sku_excel_formulas y av_ibomi_result)

**Query 1.5.1** — Estructura y datos de tablas auxiliares:
```sql
\d sku_excel_formulas
SELECT * FROM sku_excel_formulas LIMIT 10;
\d av_ibomi_result
SELECT * FROM av_ibomi_result LIMIT 10;
```

**Hallazgo 1.5.1:** Estas tablas existen pero no son parte del flujo de aprobación de fórmulas. `sku_excel_formulas` almacena fórmulas importadas desde Excel y `av_ibomi_result` parece ser una vista de resultados de negocio. No contienen campos de aprobación relevantes para este análisis.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 1

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `tformula_` solo tiene `estado` genérico, sin campos de aprobación | 1.2.1 y 1.3.1 | Odoo debe crear un modelo separado para el trámite de aprobación |
| 2 | Existe configuración multinivel (`maprob1f`/`maprobniv`) con niveles como JEFATURA, GERENCIA, DIRECCION | 1.2.3 y 1.2.4 | Odoo puede reutilizar esta lógica de niveles |
| 3 | No hay triggers en ninguna tabla de fórmulas/aprobación | 1.4.1 | Toda la lógica debe implementarse en Python/Odoo |
| 4 | Algunas compañías no tienen niveles configurados (campo `nivel` vacío en `maprobniv`) | 1.2.3 | Odoo debe validar que la compañía tenga niveles antes de iniciar trámite |
| 5 | `tmp_aprob_ped` existe como cola de pedidos pendientes | 1.2.2 | Patrón reusable para fórmulas pendientes de aprobación |

---

## 2. AUDITORÍA ESTRUCTURAL DE LÓGICA DE NEGOCIO, PROCEDIMIENTOS ALMACENADOS Y TRAZABILIDAD DINÁMICA

**Objetivo:** Analizar la distribución de estados de fórmulas, identificar dependencias en el esquema mediante muestreo de columnas de autorización (`aprob`, `autoriz`, `firm`) y auditar rutinas/funciones internas que procesan los cálculos de aprobación.

---

### 2.1 Consulta: Estados y conteo de fórmulas

**Query 2.1.1** — Distribución de estados en `tformula_`:
```sql
SELECT estado, COUNT(*) FROM tformula_ GROUP BY estado;

 estado | count 
--------+-------
  A      |  5087
(1 row)
```

**Hallazgo 2.1.1:** Todas las 5,087 fórmulas tienen `estado = 'A'` (Activo). No hay registros en estado pendiente, rechazado o borrador — la tabla no gestiona un ciclo de vida, solo almacena lo que ya está vigente.

---

### 2.2 Consulta: Tablas relacionadas con fórmulas

**Query 2.2.1** — Búsqueda de tablas con nombres tipo fórmula:
```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND (tablename ILIKE '%formula%' OR tablename ILIKE '%fml%');

     tablename      
--------------------
  tformula_
  sku_excel_formulas
(2 rows)
```

**Hallazgo 2.2.1:** Solo existen 2 tablas con "formula" en el nombre. No hay tablas tipo `tformula_hist`, `tformula_log` ni variantes — no hay historial de cambios de fórmulas en tablas dedicadas.

---

### 2.3 Consulta: Columnas de aprobación en todo el esquema

**Query 2.3.1** — Muestreo inteligente de columnas de autorización en todo `public`:
```sql
SELECT table_name, column_name 
FROM information_schema.columns 
WHERE (column_name ILIKE '%aprob%' OR column_name ILIKE '%autoriz%' OR column_name ILIKE '%visto%' OR column_name ILIKE '%firm%') 
AND table_schema = 'public' 
ORDER BY table_name;

         table_name         |     column_name      
----------------------------+----------------------
  aprfor1f                   | aprobador
  aprfor1f                   | tipaprob
  aprinv1f                   | aprobador
  aprinv2f                   | stsaprob
  aprinv2f                   | horautoriz
  aprinv2f                   | fecautoriz
  auditlote                  | aprobadop
  auditlote                  | fecaprob
  auditlote                  | horaprob
  bcktordco1f_11022021       | fecaprobac
  bcktordco1f_11022021       | desaprobp
  bcktordco1f_11022021       | ordautoriz
  bcktordco1f_11022021       | aprobadop
  bcktordco1f_11022021       | horaprobac
  ...
  maprob2f                   | cantaprob
  maprob3f                   | nivaprob
  maprob3f                   | qautoriza
  ...
  tordgr1f                   | fecaprobac
  tordgr1f                   | ordautoriz
  tordpa1f                   | desaprobp
  tordpa1f                   | aprobadop
  tordpa1f                   | ordautoriz
  ...
  v_mlpvta1f                 | horaprobac
  v_mlpvta1f                 | aprobadop
  v_tpedid1f_encabezado      | aprobadop
  v_tpedid1f_encabezado      | desaprobp
  v_tpedid1f_encabezado      | fecaprobac
  v_tpedid1f_encabezado      | horaprobac
  ws_customer_abc            | idaprobador
(491 rows)
```

**Hallazgo 2.3.1:** Se identificaron **491 columnas de aprobación distribuidas en ~150 tablas** del esquema public. El patrón de aprobación multinivel es transversal a todo el sistema (compras, inventarios, contabilidad, producción), no exclusivo de fórmulas. Los nombres de columna más recurrentes son: `aprobadop`, `fecaprobac`, `horaprobac`, `desaprobp`, `ordautoriz`, `empleautor`, `fecautoriz`.

---

### 2.4 Consulta: Funciones y procedimientos almacenados

**Query 2.4.1** — Rutinas relacionadas con aprobación o fórmulas:
```sql
SELECT routine_name, routine_type 
FROM information_schema.routines 
WHERE routine_schema = 'public' AND (routine_name ILIKE '%formula%' OR routine_name ILIKE '%aprob%');

              routine_name               | routine_type 
-----------------------------------------+--------------
  fc_obtener_nivel_aprob_ajusteinv        | FUNCTION
  fc_retornacantidadasientomanualaprobado | FUNCTION
(2 rows)
```

**Hallazgo 2.4.1:** Solo existen **2 funciones almacenadas** relacionadas con aprobación y ninguna es específica de fórmulas de producción (`fc_obtener_nivel_aprob_ajusteinv` es para ajustes de inventario, `fc_retornacantidadasientomanualaprobado` es contable). No hay procedimientos almacenados que calculen aprobación de fórmulas.

---

### 2.5 Consulta: Tablas de auditoría y logs

**Query 2.5.1** — Tablas de log/historial disponibles:
```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND (tablename ILIKE '%log%' OR tablename ILIKE '%hist%');

       tablename        
------------------------
  ajt_log_importacion
  mopelog1f
  hh_log
  hh_log_import_to_magic
  his_log_history_alert
  logconfalm
  log_cade_queque_mrp
  log_aproaje
  log_cade_queque
  logerrorescadena
  mperhist1f
  tcovta2f_log
  mvsbipplog
  pv_log_error_mx
  qv_costo_log
  scmlogs
  temp_log_rdg
  catalogos_factura_mx
  tclie19log
  mvsbsegcliprolog
  tp_logflow
  tsegclilog
 (22 rows)
```

**Hallazgo 2.5.1:** Existen **22 tablas de log/historial** disponibles para auditoría. La más relevante para este análisis es `log_aproaje` (log de aprobaciones), que se inspecciona en secciones posteriores.

---

### Resumen Sección 2

Las queries de esta sección responden a: **"¿Existe lógica de aprobación de fórmulas embebida en la base de datos (triggers, funciones, procedimientos) o hay tablas de historial?"**

- **Query 2.1** — Todas las fórmulas están activas (`estado='A'`), sin ciclo de vida visible.
- **Query 2.2** — Solo 2 tablas con "formula" en el nombre, sin historial dedicado.
- **Query 2.3** — 491 columnas de aprobación en ~150 tablas: el patrón es transversal a todo el ERP.
- **Query 2.4** — Solo 2 funciones almacenadas, ninguna de fórmulas.
- **Query 2.5** — 22 tablas de log disponibles, `log_aproaje` es la más relevante.

**Conclusión:** No hay lógica de aprobación de fórmulas en la capa de base de datos. Todo reside en la aplicación.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 2

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Todas las 5,087 fórmulas tienen `estado='A'`, sin ciclo de vida | 2.1.1 | Odoo debe definir estados (draft → pending → approved) desde cero |
| 2 | Solo 2 tablas con "formula" en el nombre, sin historial | 2.2.1 | No hay tablas de historial de fórmulas que migrar |
| 3 | 491 columnas de aprobación en ~150 tablas — patrón transversal | 2.3.1 | El modelo de aprobación de Odoo puede ser genérico y reutilizable |
| 4 | Solo 2 funciones almacenadas, ninguna de fórmulas | 2.4.1 | Toda la lógica de aprobación va en Python/Odoo |
| 5 | 22 tablas de log disponibles, `log_aproaje` es la más relevante | 2.5.1 | Odoo usará su propio Chatter para auditoría de fórmulas |

---

## 3. AUDITORÍA DE DICCIONARIOS TÉCNICOS Y LOGS DE TRANSACCIONALIDAD

**Objetivo:** Inspeccionar la estructura de las tablas maestras de configuración (`aprfor1f`), el registro histórico de firmas (`taprform1f`) y los logs de aprobación (`log_aproaje`) para garantizar que la persistencia de datos sea coherente con el flujo de Odoo 19.

### 3.1 Consulta: Tabla maestra de configuración de aprobadores (`aprfor1f`)

**Query 3.1.1** — Estructura de `aprfor1f`:
```sql
\d aprfor1f

                 Table "public.aprfor1f"
    Column   |  Type   | Collation | Nullable | Default 
 ------------+---------+-----------+----------+---------
  compania   | text    |           |          | 
  transaccio | text    |           |          | 
  nivel      | integer |           |          | 
  tipaprob   | text    |           |          | 
  aprobador  | integer |           |          | 
  estado     | text    |           |          | 
  feccrea    | integer |           |          | 
  horcrea    | text    |           |          | 
  usucrea    | text    |           |          | 
  fecultmod  | integer |           |          | 
  horultmod  | text    |           |          | 
  ultusumod  | text    |           |          | 
 Indexes:
     "idx_163675_aprfor1l1" UNIQUE, btree (compania, transaccio, nivel, tipaprob, aprobador)
```

**Hallazgo 3.1.1:** `aprfor1f` define quién puede aprobar por compañía, transacción, nivel y tipo de aprobador. Su índice único (`compania, transaccio, nivel, tipaprob, aprobador`) confirma que un mismo aprobador puede existir en múltiples niveles para una misma transacción.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 3

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `aprfor1f` define aprobadores por compañía/transacción/nivel | 3.1.1 | Odoo debe crear su propio catálogo de aprobadores |

---

## 4. HISTORIAL DE FIRMAS Y TRAZABILIDAD

**Objetivo:** Identificar quién autorizó, en qué fecha y qué datos temporales se usaron durante el proceso de aprobación de fórmulas.

### 4.1 Consulta: Histórico de firmas (`taprform1f`)

**Query 4.1.1** — Estructura de `taprform1f`:
```sql
\d taprform1f

                    Table "public.taprform1f"
    Column    |       Type       | Collation | Nullable | Default 
 -------------+------------------+-----------+----------+---------
  compania    | text             |           |          | 
  transaccio  | text             |           |          | 
  nrodoc      | text             |           |          | 
  articulo    | double precision |           |          | 
  insumo      | double precision |           |          | 
  sucform     | text             |           |          | 
  lineainsumo | text             |           |          | 
  nivel       | integer          |           |          | 
  empleautor  | integer          |           |          | 
  fecautoriz  | integer          |           |          | 
  horautoriz  | text             |           |          | 
  stsaprobac  | text             |           |          | 
  observac    | text             |           |          | 
  estado      | text             |           |          | 
  feccrea     | integer          |           |          | 
  horcrea     | text             |           |          | 
  usucrea     | text             |           |          | 
  fecultmod   | integer          |           |          | 
  horultimod  | text             |           |          | 
  ultusumod   | text             |           |          | 
 Indexes:
     "idx_173721_taprform1l1" UNIQUE, btree (compania, transaccio, nrodoc, articulo, insumo, sucform, nivel)
```

**Query 4.1.2** — Muestreo de `taprform1f`:
```sql
SELECT * FROM taprform1f LIMIT 5;

 compania | transaccio | nrodoc | articulo | insumo | sucform | lineainsumo | nivel | empleautor | fecautoriz | horautoriz | stsaprobac | observac | estado | feccrea | horcrea | usucrea | fecultmod | horultimod | ultusumod 
 ----------+------------+--------+----------+--------+---------+-------------+-------+------------+------------+------------+------------+----------+--------+---------+---------+---------+-----------+------------+-----------
 (0 rows)
```

**Hallazgo 4.1.1:** `taprform1f` debería contener el histórico de firmas por nivel de aprobación (quién autorizó, cuándo, qué estado). **La tabla está completamente vacía (0 registros).**

---

### 4.2 Consulta: Datos temporales del proceso (`tmpdetfor`)

**Query 4.2.1** — Estructura de `tmpdetfor`:
```sql
\d tmpdetfor

                     Table "public.tmpdetfor"
     Column    |       Type       | Collation | Nullable | Default 
 --------------+------------------+-----------+----------+---------
  clave        | text             |           |          | 
  compania     | text             |           |          | 
  transaccio   | text             |           |          | 
  nrodoc       | text             |           |          | 
  sucform      | text             |           |          | 
  articulo     | double precision |           |          | 
  insumo       | double precision |           |          | 
  linea        | text             |           |          | 
  factconv     | double precision |           |          | 
  accion       | text             |           |          | 
  nivapro      | smallint         |           |          | 
  flgaprob     | boolean          |           |          | 
  aprobadop    | integer          |           |          | 
  fecaprob     | integer          |           |          | 
  horaprob     | text             |           |          | 
  stssolicitud | text             |           |          | 
  progactfor   | text             |           |          | 
  seleccion    | bytea            |           |          | 
  elimreg      | boolean          |           |          | 
 Indexes:
     "idx_177299_tmpdetforl1" UNIQUE, btree (clave, compania, transaccio, nrodoc, sucform, articulo, insumo)
     "idx_177299_tmpdetforl2" btree (clave, seleccion, compania, transaccio, nrodoc, sucform, articulo, insumo)
```

**Query 4.2.2** — Muestreo de `tmpdetfor`:
```sql
SELECT * FROM tmpdetfor LIMIT 5;

 clave | compania | transaccio | nrodoc | sucform | articulo | insumo | linea | factconv | accion | nivapro | flgaprob | aprobadop | fecaprob | horaprob | stssolicitud | progactfor | seleccion | elimreg 
 -------+----------+------------+--------+---------+----------+--------+-------+----------+--------+---------+----------+-----------+----------+----------+--------------+------------+-----------+---------
 (0 rows)
```

**Hallazgo 4.2.1:** `tmpdetfor` almacena los datos temporales del proceso de solicitud (acción a realizar, flag de aprobación, aprobador, fecha/hora). **También está vacía (0 registros).**

**Resumen**

"Consultamos `taprform1f` (debería tener el histórico de firmas por nivel) y `tmpdetfor` (debería tener los datos temporales de cada solicitud). Ambas están en cero. Esto confirma que el flujo multinivel de aprobación de fórmulas nunca se operó en Mexico — la aprobación se ejecuta por una vía directa sin pasar por estas tablas de trámite."

---

### RESUMEN DE HALLAZGOS — SECCIÓN 4

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `taprform1f` (histórico de firmas) está vacía — 0 registros | 4.1.2 | No hay historial de firmas que migrar |
| 2 | `tmpdetfor` (datos temporales del proceso) está vacía — 0 registros | 4.2.2 | El flujo de trámite nunca se operó |

---

## 5. MAESTRO DE FÓRMULAS DE FABRICACIÓN (`forfab`)

**Objetivo:** Verificar si los cambios aprobados impactan directamente en esta tabla, que es la que usa producción.

### 5.1 Consulta: Estructura y datos de `forfab`

**Query 5.1.1** — Estructura de `forfab`:
```sql
\d forfab

                      Table "public.forfab"
     Column    |       Type       | Collation | Nullable | Default 
 --------------+------------------+-----------+----------+---------
  compania     | text             |           | not null | 
  sucursal     | text             |           | not null | 
  articulo     | double precision |           | not null | 
  nrosecu      | smallint         |           | not null | 
  material     | double precision |           | not null | 
  porcent      | double precision |           | not null | 
  factconv     | double precision |           | not null | 
  cantidad     | double precision |           | not null | 
  stkdisp      | double precision |           | not null | 
  tipdist      | text             |           | not null | 
  fase         | integer          |           | not null | 
  corrfase     | smallint         |           | not null | 
  feccrea      | integer          |           | not null | 
  horcrea      | text             |           | not null | 
  usucrea      | text             |           | not null | 
  ultfecmod    | integer          |           | not null | 
  ulthormod    | text             |           | not null | 
  ultusumod    | text             |           | not null | 
  lanza        | bytea            |           | not null | 
  tetiqueta    | text             |           |          | 
  aprobadop    | integer          |           |          | 
  fecaprobadop | integer          |           |          | 
  horaprobadop | text             |           |          | 
 Indexes:
     "idx_167195_forfab01" UNIQUE, btree (compania, sucursal, articulo, material)
     "idx_167195_forfab02" btree (compania, sucursal, material, articulo)
```

**Query 5.1.2** — Muestreo de `forfab`:
```sql
SELECT * FROM forfab LIMIT 5;

 compania | sucursal | articulo | nrosecu | material | porcent | factconv  | cantidad  | stkdisp | tipdist | fase | corrfase | feccrea | horcrea | usucrea  | ultfecmod | ulthormod | ultusumod | lanza | tetiqueta | aprobadop | fecaprobadop | horaprobadop 
 ----------+----------+----------+---------+----------+---------+-----------+-----------+---------+---------+------+----------+---------+---------+----------+-----------+-----------+-----------+-------+-----------+-----------+--------------+--------------
  0030     | 0001     |   524121 |       1 |     7177 |     100 |      18.8 |     59220 |       0 | UA      |    0 |        0 |  739494 | 070149  | MGLUNA   |    739494 | 070149    | MGLUNA    | \x54  |           |   1724308 |            0 | 000000
  0030     | 0068     |   517262 |       1 |        8 |     100 | 0.0892054 | 633.62596 |       0 | UA      |    0 |        0 |  739632 | 100252  | MGLUNA   |    739632 | 100252    | MGLUNA    | \x54  |           |   1724308 |       739632 | 101951
  0030     | 0001     |    81388 |       1 |    71741 |     100 | 0.0001968 |    0.1968 |       0 | UA      |    0 |        0 |  739458 | 110842  | AHRIVERA |    739458 | 110842    | AHRIVERA  | \x54  |           |     29750 |       739458 | 112102
  0030     | 0001     |    58173 |       1 |    47279 |     100 |      0.49 |       490 |       0 | UC      |    0 |        0 |  739447 | 093624  | AHRIVERA |    739447 | 093624    | AHRIVERA  | \x54  |           |     29750 |            0 | 000000
  0030     | 0001     |    68536 |       2 |    47279 |     100 |      0.49 |       490 |       0 | UA      |    2 |        2 |  739052 | 085732  | AHRIVERA |    739052 | 085732    | AHRIVERA  | \x54  |           |     29750 |            0 | 000000
 (5 rows)
```

**Hallazgo 5.1.1:** `forfab` contiene 70,070 fórmulas activas con IDs de aprobadores reales (ej: 1724308, 29750). Sin embargo, las columnas `fecaprobadop` y `horaprobadop` aparecen vacías o con valores cero en la mayoría de registros — se sabe quién aprobó pero no cuándo. Evidencia una carencia de auditoría temporal en el sistema legacy.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 5

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `forfab` tiene 70,070 fórmulas con aprobador pero sin fecha/hora de aprobación | 5.1.2 | Odoo debe forzar registro de fecha/hora al aprobar |

---

## 6. SOLICITUDES DE ACTIVACIÓN DE FÓRMULAS

**Objetivo:** Analizar el documento de solicitud (Cabecera/Detalle) que se crea ANTES de que la fórmula sea oficial.

### 6.1 Consulta: Cabecera de solicitud (`csolactfor`)

**Query 6.1.1** — Estructura de `csolactfor`:
```sql
\d csolactfor

                 Table "public.csolactfor"
     Column     |  Type   | Collation | Nullable | Default 
 ----------------+---------+-----------+----------+---------
  compania       | text    |           |          | 
  transaccio     | text    |           |          | 
  nrodoc         | text    |           |          | 
  fecha          | integer |           |          | 
  solicitante    | integer |           |          | 
  qarticulos     | integer |           |          | 
  qacciones      | integer |           |          | 
  flgmailenviado | bytea   |           |          | 
  nivelapr       | integer |           |          | 
  aprobador      | integer |           |          | 
  fecaprobac     | integer |           |          | 
  horaprobac     | text    |           |          | 
  stsaprobac     | text    |           |          | 
  stsactualiza   | text    |           |          | 
  flganulado     | bytea   |           |          | 
  fecanula       | integer |           |          | 
  feccrea        | integer |           |          | 
  horcrea        | text    |           |          | 
  usucrea        | text    |           |          | 
  fecultmod      | integer |           |          | 
  horultmod      | text    |           |          | 
  ultusumod      | text    |           |          | 
 Indexes:
     "idx_165818_csolactforl1" UNIQUE, btree (compania, transaccio, nrodoc)
```

### 6.2 Consulta: Detalle de solicitud (`dsolactfor`)

**Query 6.2.1** — Estructura de `dsolactfor`:
```sql
\d dsolactfor

                     Table "public.dsolactfor"
     Column    |       Type       | Collation | Nullable | Default 
 --------------+------------------+-----------+----------+---------
  compania     | text             |           |          | 
  transaccio   | text             |           |          | 
  nrodoc       | text             |           |          | 
  sucform      | text             |           |          | 
  articulo     | double precision |           |          | 
  insumo       | double precision |           |          | 
  lineainsumo  | text             |           |          | 
  factconv     | double precision |           |          | 
  accion       | text             |           |          | 
  nivaprob     | integer          |           |          | 
  flgaprob     | bytea            |           |          | 
  aprobadop    | integer          |           |          | 
  fecaprob     | integer          |           |          | 
  horaprob     | text             |           |          | 
  stsaprobac   | text             |           |          | 
  stsactualiza | text             |           |          | 
  feccrea      | integer          |           |          | 
  horcrea      | text             |           |          | 
  usucrea      | text             |           |          | 
  fecultmod    | integer          |           |          | 
  horultmod    | text             |           |          | 
  ultusumod    | text             |           |          | 
 Indexes:
     "idx_166686_dsolactforl1" UNIQUE, btree (compania, transaccio, nrodoc, sucform, articulo, insumo)
```

**Query 6.2.2** — Muestreo de `csolactfor`:
```sql
SELECT * FROM csolactfor LIMIT 5;

 compania | transaccio | nrodoc | fecha | solicitante | qarticulos | qacciones | flgmailenviado | nivelapr | aprobador | fecaprobac | horaprobac | stsaprobac | stsactualiza | flganulado | fecanula | feccrea | horcrea | usucrea | fecultmod | horultmod | ultusumod 
 ----------+------------+--------+-------+-------------+------------+-----------+----------------+----------+-----------+------------+------------+------------+--------------+------------+----------+---------+---------+---------+-----------+-----------+-----------
 (0 rows)
```

**Hallazgo 6.2.1:** `csolactfor` y `dsolactfor` están vacías (0 registros). Estas tablas deberían contener las solicitudes de activación de fórmulas (cabecera y detalle) antes de que sean oficiales. Su vacío confirma que en Mexico no se usa el flujo de solicitud formal — las fórmulas se crean y aprueban directamente sin pasar por este trámite.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 6

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `csolactfor`/`dsolactfor` (solicitudes de activación) vacías | 6.2.2 | No se usa flujo de solicitud formal en Mexico |

---

## 7. BITÁCORA DE AUDITORÍA Y CAMBIOS DE ESTADO

**Objetivo:** Ver el rastro de quién cambió los estados de aprobación y detectar si hay reversiones o rechazos.

### 7.1 Consulta: Log de aprobaciones (`log_aproaje`)

**Query 7.1.1** — Estructura de `log_aproaje`:
```sql
\d log_aproaje

                                       Table "public.log_aproaje"
   Column  |            Type             | Collation | Nullable |                 Default                 
 ----------+-----------------------------+-----------+----------+-----------------------------------------
  id       | bigint                      |           | not null | nextval('log_aproaje_id_seq'::regclass)
  jsonbody | text                        |           |          | 
  idapp    | integer                     |           |          | 
  response | text                        |           |          | 
  fecha    | timestamp without time zone |           |          | 
 Indexes:
     "idx_167765_pk__log_apro__3214ec273bf6f9fd" PRIMARY KEY, btree (id)
```

**Query 7.1.2** — Muestreo de `log_aproaje`:
```sql
SELECT * FROM log_aproaje LIMIT 5;

 id | jsonbody
 ----+---------
  1 | {"auth":"areli.torres.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000020","detail": {"title":"AJEMEX - 0001 : PLANTA PUEBLA/202506000020","body": [{"campo":"Compania","valor":"0030 - AJEMEX"},{"campo":"Sucursal","valor":"0001 - PLANTA PUEBLA"},{"campo":"Numero Documento","valor":"202506000020"},{"campo":"Solicitante","valor":"GARCIA MINERO LUISA"},{"campo":"Fecha","valor":"27/06/2025"},{"campo":"Moneda","valor":"PES - PESOS"},{"campo":"Importe","valor":"85000.00"},{"campo":"Glosa","valor":"CANCELACION DE PROV DE GTOS DE IMPORTACION EXP 141 AJEMAYA OC 139549"},{"campo":"PRIMERA APROBACION","valor":"APROBACION"},{"campo":"Aprobador","valor":"TORRES SANCHEZ MARIA SURIARELI"}],"details_title":"DETALLE","details_header": [{"titulo":"Cuenta Contable","width":"80"},{"titulo":"Descripcion","width":"400"},{"titulo":"Dolares","width":"80"},{"titulo":"Debe","width":"80"},{"titulo":"Haber","width":"80"}],"details_rows": [...]},...
  2 | {"auth":"yazmin.ramirez.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000020",...
  3 | {"auth":"areli.torres.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021",...
  4 | {"auth":"yazmin.ramirez.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021",...
  5 | {"auth":"areli.torres.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021",...
 (5 rows)
```

**Hallazgo 7.1.1:** `log_aproaje` contiene registros JSON de auditoría, pero corresponden a aprobaciones de **asientos contables manuales** (nemotecnico: `AprobacionAsientoManual`, type: `AMA`), no a fórmulas de producción. Cada registro incluye email del aprobador, detalles del documento y campos de validación. Esta tabla es un log genérico del sistema de aprobaciones, no específico del programa #162.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 7

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `log_aproaje` es log genérico de asientos contables, no de fórmulas | 7.1.2 | Odoo usará Chatter para auditoría específica de fórmulas |

---

## 8. ANÁLISIS TÉCNICO DE REGLAS DE NEGOCIO Y CICLO DE VIDA

**Objetivo:** Mapear los estados (`stsaprobac`) para configurar el State Machine de Odoo 19 y diferenciar borradores de aprobados. Identificar el ID de transacción para aislar Producción de otros módulos. Cuantificar registros para prever carga en Chatter e historial.

### 8.1 Consulta: Mapeo de estados y transacciones

**Query 8.1.1** — Estados, transacciones y tipos de aprobación:
```sql
SELECT DISTINCT stsaprobac, 'En Solicitudes (csolactfor)' as procedencia FROM csolactfor;
SELECT DISTINCT stsaprobac, 'En Histórico Firmas (taprform1f)' as procedencia FROM taprform1f;
SELECT DISTINCT transaccio, 'ID de proceso en csolactfor' as nota FROM csolactfor;
SELECT DISTINCT tipaprob, 'Tipos de aprobadores en aprfor1f' as nota FROM aprfor1f;
SELECT DISTINCT accion as tipo_operacion, 'Lógica de cambio en tmpdetfor' as contexto FROM tmpdetfor;
SELECT DISTINCT stssolicitud as estado_sincro, 'Estado integración tmpdetfor' as contexto FROM tmpdetfor;

 stsaprobac | procedencia 
 ------------+-------------
(0 rows)

 stsaprobac | procedencia 
 ------------+-------------
(0 rows)

 transaccio | nota 
 ------------+------
(0 rows)

 tipaprob | nota 
 ----------+------
(0 rows)

 tipo_operacion | contexto 
 ----------------+----------
(0 rows)

 estado_sincro | contexto 
 ---------------+----------
(0 rows)
```

### 8.2 Consulta: Cuantificación de registros

**Query 8.2.1** — Conteo de objetos:
```sql
SELECT 'Solicitudes de Activación' as objeto, COUNT(*) as total FROM csolactfor;
SELECT 'Firmas y Logs históricos' as objeto, COUNT(*) as total FROM taprform1f;
SELECT 'Fórmulas finales en producción' as objeto, COUNT(*) as total FROM forfab;

          objeto           | total 
 ---------------------------+-------
 Solicitudes de Activación |     0
(1 row)

          objeto          | total 
 --------------------------+-------
 Firmas y Logs históricos |     0
(1 row)

             objeto             | total 
 --------------------------------+-------
 Fórmulas finales en producción | 70070
(1 row)
```

**Hallazgo 8.2.1:** Todas las consultas de estados, transacciones y tipos de aprobación retornan 0 rows, confirmando que las tablas de trámite (`csolactfor`, `taprform1f`, `tmpdetfor`, `aprfor1f`) no tienen datos operativos para fórmulas de producción. El único dato relevante: `forfab` tiene 70,070 fórmulas finales. **No hay estados que mapear para el State Machine de Odoo desde las tablas legacy** — los estados (draft → pending → approved) se definirán desde cero.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 8

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | No hay estados (`stsaprobac`) que mapear — todas las tablas de trámite en 0 | 8.1.1 | State Machine de Odoo se define desde cero (draft → pending → approved) |
| 2 | `forfab` tiene 70,070 fórmulas finales | 8.2.1 | Volumen conocido para planificar migración |

---

## 9. INVESTIGACIÓN DE FIRMAS DIRECTAS EN MAESTRO DE PRODUCCIÓN

**Objetivo:** Debido a que las tablas de trámite están vacías, se valida si la aprobación se registra directamente en el maestro mediante IDs de usuario.

### 9.1 Consulta: IDs de aprobadores en `forfab`

**Query 9.1.1** — IDs de aprobadores detectados:
```sql
SELECT DISTINCT aprobadop, 'ID Aprobador detectado' as metadato 
FROM forfab 
WHERE aprobadop IS NOT NULL AND aprobadop > 0 
LIMIT 10;

 aprobadop |        metadato        
 -----------+------------------------
    1708248 | ID Aprobador detectado
       6881 | ID Aprobador detectado
    1683322 | ID Aprobador detectado
      29750 | ID Aprobador detectado
    1668443 | ID Aprobador detectado
    1668285 | ID Aprobador detectado
    1657091 | ID Aprobador detectado
      64435 | ID Aprobador detectado
    1779648 | ID Aprobador detectado
    1721708 | ID Aprobador detectado
 (10 rows)
```

### 9.2 Consulta: Trazabilidad de aprobaciones

**Query 9.2.1** — Muestra de trazabilidad:
```sql
SELECT compania, articulo, material, aprobadop, fecaprobadop, horaprobadop 
FROM forfab 
WHERE aprobadop IS NOT NULL AND aprobadop > 0 
ORDER BY fecaprobadop DESC 
LIMIT 5;

 compania | articulo | material | aprobadop | fecaprobadop | horaprobadop 
 ----------+----------+----------+-----------+--------------+--------------
  0030     |    73145 |    73147 |   1708248 |              | 
  0030     |    73145 |    73148 |   1708248 |              | 
  0030     |    73278 |    20210 |   1708248 |              | 
  0030     |    73145 |    73146 |   1708248 |              | 
  0030     |    73145 |    26198 |   1708248 |              | 
 (5 rows)
```

**Hallazgo 9.2.1:** Se confirma que la aprobación se persiste directamente en el maestro de producción `forfab`. Sin embargo, las columnas `fecaprobadop` y `horaprobadop` aparecen vacías en los registros recientes, lo que sugiere que el sistema original podría estar delegando la fecha a otra tabla de logs o que el trigger de actualización no se disparó. **Odoo deberá forzar el llenado de estos campos para mantener la integridad.**

---

### RESUMEN DE HALLAZGOS — SECCIÓN 9

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Aprobación directa en `forfab` con IDs pero sin trazabilidad temporal | 9.2.1 | Odoo debe implementar auditoría completa (quién, cuándo, observaciones) |
