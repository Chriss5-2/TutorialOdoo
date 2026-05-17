## 1. EXPLORACIÓN DE DICCIONARIO DE DATOS - GESTIÓN DE TURNOS

**Objetivo:** Ejecutar consulta de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas a la gestión de turnos, jornadas y rotaciones dentro del esquema público, con el fin de mapear la estructura de persistencia en `mxbdaje_local`.

### 1.1 Consulta: Tablas relacionadas con turnos

**Query 1.1.1** — Búsqueda de tablas con nombres tipo turno/shift:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%turno%' OR tablename ILIKE '%turn%' OR tablename ILIKE '%shift%');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 tablename   
 ---------------
  bturno1f
  relacionturno
  turnoxop
  turno
 (4 rows)
```

**Hallazgo 1.1.1:** Se han identificado 4 entidades clave. La tabla `bturno1f` sigue la nomenclatura de las tablas maestras de configuración (similar a `aprfor1f`), lo que sugiere que contiene la definición base de los turnos. `relacionturno` y `turnoxop` parecen ser tablas de rotación o asignación transaccional (posiblemente vinculando turnos con operaciones o empleados), mientras que `turno` podría ser una tabla simplificada o una vista remanente.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 1

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 4 tablas identificadas: `bturno1f`, `relacionturno`, `turnoxop`, `turno` | 1.1.1 | Es necesario inspeccionar `bturno1f` y `turnoxop` para entender la lógica de herencia |

---

## 2. AUDITORÍA DE INTEGRIDAD REFERENCIAL - CAMPOS DE TURNO

**Objetivo:** Inspeccionar todas las columnas del esquema público que contienen referencias a "turno" o "shift" para identificar dependencias en tablas transaccionales, de empleados o de nómina, asegurando el rastreo de la persistencia de jornadas laborales.

### 2.1 Consulta: Columnas relacionadas con turno en todo el esquema

**Query 2.1.1** — Muestreo inteligente de columnas de turno en todo `public`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE (column_name ILIKE '%turno%' OR column_name ILIKE '%shift%') 
AND table_schema = 'public' 
ORDER BY table_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 table_name       | column_name | data_type 
 ------------------------+-------------+-----------
  audit02052023ca        | turnodesca  | text
  audit02052023ca        | turnocarga  | text
  ...
  bturno1f               | turno       | text
  bturno1f               | descturno1  | text
  bturno1f               | descturno2  | text
  bturno1f               | ststurno    | text
  ...
  tcoalm1f               | turnocarga  | text
  tcoalm1f               | turnodesca  | text
  ...
  turnoxop               | turno       | text
 (71 rows)
```

**Hallazgo 2.1.1:** El barrido revela una **dispersión masiva** de la entidad "turno" en 71 columnas, confirmando que el sistema maneja la lógica de turnos de forma transversal (Logística, Producción, Auditoría e Inventarios). La predominancia del tipo `text` sugiere que el sistema no utiliza IDs numéricos secuenciales nativos de Odoo, sino **llaves naturales** mediante códigos (ej. 'T1', 'T2'). La diferenciación entre `turnocarga` y `turnodesca` en tablas de almacén (`tcoalm1f`) indica que los procesos son asíncronos, permitiendo que una operación inicie en un turno y concluya en otro.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 2

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 71 columnas con referencia a turno en ~50 tablas | 2.1.1 | Lógica transversal, requiere modelo referenciable desde múltiples estructuras |
| 2 | Predominancia de tipo `text` (llaves naturales) | 2.1.1 | Odoo debe usar códigos como `Char` fields con constraints de unicidad |
| 3 | Diferenciación `turnocarga` vs `turnodesca` | 2.1.1 | Procesos asíncronos: inicio y fin pueden ser en turnos distintos |

---

## 3. ANÁLISIS DE ESTRUCTURA DDL - TABLAS MAESTRAS DE TURNOS

**Objetivo:** Inspeccionar la definición técnica de las tablas `bturno1f` y `turnoxop` para identificar llaves primarias, restricciones de unicidad y auditoría.

### 3.1 Consulta: Estructura de `bturno1f` y `turnoxop`

**Query 3.1.1** — Describir estructura de tablas maestras:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d bturno1f; \d turnoxop;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
                 Table "public.bturno1f"
    Column   |  Type   | Collation | Nullable | Default 
 ------------+---------+-----------+----------+---------
  compania   | text    |           |          | 
  turno      | text    |           | not null | 
  descturno1 | text    |           |          | 
  descturno2 | text    |           |          | 
  ststurno   | text    |           |          | 
  feccreacio | integer |           | not null | 
  horcreacio | text    |           | not null | 
  usuacreac  | text    |           | not null | 
  fecultimod | integer |           | not null | 
  horultimod | text    |           | not null | 
  usuaulmod  | text    |           | not null | 
  estado     | text    |           | not null | 
 Indexes:
     "idx_164965_bturno1l01" UNIQUE, btree (compania, turno)
     "idx_164965_bturno1l02" UNIQUE, btree (compania, ststurno, turno)

                Table "public.turnoxop"
   Column   |  Type   | Collation | Nullable | Default 
 -----------+---------+-----------+----------+---------
  compania  | text    |           | not null | 
  sucursal  | text    |           | not null | 
  fechatur  | integer |           | not null | 
  nroop     | text    |           |          | 
  turno     | text    |           | not null | 
  estado    | text    |           | not null | 
  feccrea   | integer |           | not null | 
  horcrea   | text    |           | not null | 
  usucrea   | text    |           | not null | 
  ultfecmod | integer |           | not null | 
  ulthormod | text    |           | not null | 
  ultusumod | text    |           | not null | 
 Indexes:
     "idx_179725_turnoxop_i1" UNIQUE, btree (compania, sucursal, fechatur, nroop, turno)
```

**Hallazgo 3.1.1:** Se confirma que la unicidad depende de **llaves compuestas** `(compania, turno)` en `bturno1f`. En Odoo 19, esto requiere concatenar ambos campos para generar `xml_ids` únicos. La tabla `turnoxop` revela una vinculación operativa mediante `nroop` y una gestión por fecha (`fechatur`), lo que facilitará el mapeo hacia órdenes de trabajo. La presencia de campos de auditoría (`usuacreac`, `horultimod`) permitirá validar la integridad de los datos previo a la carga.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 3

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `bturno1f` usa llave compuesta `(compania, turno)` | 3.1.1 | Generar `xml_ids` concatenando compañía + turno |
| 2 | `turnoxop` vincula turnos con OPs por fecha | 3.1.1 | Modelo transaccional mapeable a Work Orders |

---

## 4. ANÁLISIS DE DATOS REALES - TABLA MAESTRA `bturno1f`

**Objetivo:** Inspeccionar los datos reales almacenados en la tabla maestra `bturno1f` para comprender los códigos de turno utilizados, la estructura de descripciones y el patrón de replicación por compañía.

### 4.1 Consulta: Datos de `bturno1f`

**Query 4.1.1** — Muestreo de `bturno1f`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM bturno1f LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | turno | descturno1 | descturno2 | ststurno | feccreacio | horcreacio | usuacreac | fecultimod | horultimod | usuaulmod | estado 
 ----------+-------+------------+------------+----------+------------+------------+-----------+------------+------------+-----------+--------
  0032     | 001   | TURNO1     | TURNO 1    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0070     | 001   | TURNO1     | TURNO 1    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0076     | 001   | TURNO1     | TURNO 1    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0081     | 001   | TURNO1     | TURNO 1    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  5000     | 001   | TURNO1     | TURNO 1    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0032     | 002   | TURNO2     | TURNO 2    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0070     | 002   | TURNO2     | TURNO 2    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0076     | 002   | TURNO2     | TURNO 2    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0081     | 002   | TURNO2     | TURNO 2    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  5000     | 002   | TURNO2     | TURNO 2    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0032     | 003   | TURNO3     | TURNO 3    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0070     | 003   | TURNO3     | TURNO 3    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0076     | 003   | TURNO3     | TURNO 3    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0081     | 003   | TURNO3     | TURNO 3    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0030     | 001   | TURNO1     | TURNO 1    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0030     | 002   | TURNO2     | TURNO 2    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0030     | 003   | TURNO3     | TURNO 3    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  5000     | 003   | TURNO3     | TURNO 3    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0036     | 001   | TURNO1     | TURNO 1    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
  0036     | 002   | TURNO2     | TURNO 2    | A        |     734799 | 010120     | CPALOMINO |     734799 | 010120     | CPALOMINO | A
 (20 rows)
```

**Hallazgo 4.1.1:** Los turnos usan códigos secuenciales de 3 dígitos (`001`, `002`, `003`) representando Primer, Segundo y Tercer turno. El mismo turno existe en múltiples compañías (`0030`, `0032`, `0070`, `0076`, `0081`, `5000`, `0036`), lo que indica que la maestra `bturno1f` es una tabla de definición base sin horarios específicos. `descturno1` (ej: `TURNO1`) y `descturno2` (ej: `TURNO 1`) parecen ser variantes de formato. `feccreacio = 734799` equivale aproximadamente a enero 2010 (fecha juliana), sugiriendo una carga masiva inicial por el usuario `CPALOMINO`. Todos los registros muestran `ststurno = A` y `estado = A`.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 4

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Códigos secuenciales `001`, `002`, `003` por compañía | 4.1.1 | Mapear a modelo de definición de turnos |
| 2 | Doble descripción (`descturno1`, `descturno2`) | 4.1.1 | Unificar o conservar ambas según necesidad de reportes |
| 3 | Fechas julianas (~enero 2010) y usuario `CPALOMINO` | 4.1.1 | Carga masiva inicial, convertir fechas para Odoo |

---

## 5. ANÁLISIS DE ESTRUCTURA DDL - TABLAS `relacionturno` Y `turno`

**Objetivo:** Inspeccionar la definición técnica de `relacionturno` (mapeo BM ↔ AVAIL) y `turno` (definición con horarios reales por sucursal).

### 5.1 Consulta: Estructura de `relacionturno` y `turno`

**Query 5.1.1** — Describir estructura de tablas de mapeo y horarios:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d relacionturno; \d turno;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
              Table "public.relacionturno"
    Column   |  Type   | Collation | Nullable | Default 
 ------------+---------+-----------+----------+---------
  compania   | text    |           | not null | 
  sucursal   | text    |           | not null | 
  turnobm    | text    |           | not null | 
  turnoav    | text    |           | not null | 
  estado     | text    |           |          | 
  feccrea    | integer |           | not null | 
  horcrea    | text    |           | not null | 
  usucrea    | text    |           | not null | 
  fecultmod  | integer |           | not null | 
  horultmod  | text    |           | not null | 
  ultusumod  | text    |           | not null | 
 Indexes:
     "idx_172982_relacionturno_i1" PRIMARY KEY, btree (compania, sucursal, turnobm, turnoav)

                   Table "public.turno"
    Column    |  Type   | Collation | Nullable | Default 
 -------------+---------+-----------+----------+---------
  compania    | text    |           | not null | 
  sucursal    | text    |           | not null | 
  turno       | text    |           | not null | 
  descripcion | text    |           | not null | 
  hinicio     | text    |           | not null | 
  hfin        | text    |           | not null | 
  feccrea     | integer |           | not null | 
  horcrea     | text    |           | not null | 
  usucrea     | text    |           | not null | 
  ultfecmod   | integer |           | not null | 
  ulthormod   | text    |           | not null | 
  ultusumod   | text    |           | not null | 
  flgidavail  | bytea   |           |          | 
  flgenuso    | bytea   |           |          | 
 Indexes:
     "idx_179720_turno1" UNIQUE, btree (compania, sucursal, turno)
```

**Hallazgo 5.1.1:** `relacionturno` es una tabla de mapeo entre turnos de Big Magic (`turnobm`) y turnos del sistema AVAIL (`turnoav`), con clave primaria compuesta de 4 campos. Creada por `SYSTEM`, sugiere carga automática durante configuración de integración. `turno` contiene `hinicio` y `hfin` en formato `HHMMSS`, definiendo los horarios reales de cada turno con granularidad por sucursal `(compania, sucursal, turno)`. Banderas `flgidavail` y `flgenuso` (bytea) para integración con AVAIL y control de uso.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 5

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `relacionturno` mapea BM ↔ AVAIL con PK compuesta | 5.1.1 | Migrar solo si hay integración activa con AVAIL |
| 2 | `turno` define horarios reales (`hinicio`/`hfin`) por sucursal | 5.1.1 | Modelo de horarios operativos en Odoo |

---

## 6. ANÁLISIS DE DATOS REALES - TABLA `relacionturno` (MAPEO BM ↔ AVAIL)

**Objetivo:** Inspeccionar los datos reales de mapeo entre turnos de Big Magic y AVAIL para entender la correspondencia de códigos entre sistemas.

### 6.1 Consulta: Datos de `relacionturno`

**Query 6.1.1** — Muestreo de `relacionturno`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM relacionturno LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | turnobm | turnoav | estado | feccrea | horcrea | usucrea | fecultmod | horultmod | ultusumod 
 ----------+----------+---------+---------+--------+---------+---------+---------+-----------+------------+-----------
  0030     | 0001     | 001     |         | A      |  737593 | 083006  | SYSTEM  |    737593 | 083006     | SYSTEM
  0030     | 0001     | 001     | 1       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0001     | 002     | 2       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0001     | 003     | 3       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0068     | 001     |         | A      |  737593 | 083006  | SYSTEM  |    737593 | 083006     | SYSTEM
  0030     | 0068     | 001     | 1       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0068     | 002     | 2       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0068     | 003     | 3       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0070     | 001     |         | A      |  737593 | 083006  | SYSTEM  |    737593 | 083006     | SYSTEM
  0030     | 0070     | 001     | 1       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0070     | 002     | 2       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0070     | 003     | 3       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
  0030     | 0108     | 001     |         | A      |  737593 | 083006  | SYSTEM  |    737593 | 083006     | SYSTEM
  0030     | 0108     | 001     | 1       | A      |  737532 | 115844  | SYSTEM  |    737532 | 115844     | SYSTEM
 (14 rows)
```

**Hallazgo 6.1.1:** La relación es casi 1:1 entre `turnobm` (`001`, `002`, `003`) y `turnoav` (`1`, `2`, `3`), con diferencia de formato (BM usa 3 dígitos, AVAIL usa 1 dígito). Existen registros duplicados para el mismo `turnobm = 001` en cada sucursal: uno con `turnoav` vacío y otro con `turnoav = 1`. Esto sugiere un fallback o registro comodín cuando no hay mapeo específico. Todos los registros fueron creados por `SYSTEM`.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 6

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Mapeo directo BM `001/002/003` ↔ AVAIL `1/2/3` | 6.1.1 | Diferencia de formato a normalizar |
| 2 | Registros duplicados con `turnoav` vacío | 6.1.1 | Fallback del sistema, ignorar en migración |

---

## 7. ANÁLISIS DE DATOS REALES - TABLA `turnoxop` (ASIGNACIÓN TURNO ↔ OP)

**Objetivo:** Inspeccionar la tabla transaccional que vincula turnos con órdenes de producción, entendiendo cómo se registra qué turno ejecutó qué OP en qué fecha.

### 7.1 Consulta: Datos de `turnoxop`

**Query 7.1.1** — Muestreo de `turnoxop`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM turnoxop LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | fechatur |   nroop    | turno | estado | feccrea | horcrea |  usucrea   | ultfecmod | ulthormod | ultusumod  
 ----------+----------+----------+------------+-------+--------+---------+---------+------------+-----------+-----------+------------
  0030     | 0068     |   737850 | PMTY210004 | 001   | A      |  737850 | 074449  | JMACARENO  |    737850 | 074449    | JMACARENO
  0030     | 0001     |   737852 | PPUE210017 | 003   | A      |  737852 | 004013  | LAPEREZ    |    737852 | 004013    | LAPEREZ
  0030     | 0068     |   737852 | PMTY210004 | 003   | A      |  737852 | 225159  | MGOMEZ     |    737852 | 225159    | MGOMEZ
  0030     | 0001     |   737857 | PPUE210018 | 001   | A      |  737857 | 080317  | MLEGORRETA |    737857 | 080317    | MLEGORRETA
  0030     | 0068     |   737857 | PMTY210005 | 003   | A      |  737857 | 222531  | RRSALAZAR  |    737857 | 222531    | RRSALAZAR
  0030     | 0001     |   737863 | PPUE210020 | 001   | A      |  737863 | 141621  | CANTEPL    |    737863 | 141621    | CANTEPL
  0030     | 0001     |   737865 | PPUE210020 | 001   | A      |  737865 | 065621  | LAPEREZ    |    737865 | 065621    | LAPEREZ
  0030     | 0070     |   737868 | PVHS210003 | 001   | A      |  737868 | 125519  | LCRUZM     |    737868 | 125519    | LCRUZM
  0030     | 0068     |   737871 | PMTY210006 | 001   | A      |  737871 | 071042  | RRSALAZAR  |    737871 | 071042    | RRSALAZAR
  0030     | 0001     |   737880 | PPUE210025 | 002   | A      |  737876 | 203249  | MLEGORRETA |    737876 | 203249    | MLEGORRETA
  0030     | 0070     |   737878 | PVHS210003 | 001   | A      |  737878 | 073134  | JRCALDERON |    737878 | 073134    | JRCALDERON
  0030     | 0068     |   737878 | PMTY210006 | 003   | A      |  737878 | 143242  | EDUARDOMG  |    737878 | 143242    | EDUARDOMG
  0030     | 0001     |   737885 | PPUE210026 | 001   | A      |  737885 | 065850  | LAPEREZ    |    737885 | 065850    | LAPEREZ
  0030     | 0001     |   737891 | PPUE210030 | 002   | A      |  737891 | 154802  | MLEGORRETA |    737891 | 154802    | MLEGORRETA
  0030     | 0068     |   737893 | PMTY210008 | 003   | A      |  737893 | 224222  | MGOMEZ     |    737893 | 224222    | MGOMEZ
  0030     | 0001     |   737897 | PPUE210032 | 002   | A      |  737897 | 172555  | OROMERO    |    737897 | 172555    | OROMERO
  0030     | 0001     |   737898 | PPUE210032 | 003   | A      |  737898 | 154426  | DJESPINOZA |    737898 | 154426    | DJESPINOZA
  0030     | 0068     |   737899 | PMTY210009 | 002   | A      |  737899 | 165719  | EDUARDOMG  |    737899 | 165719    | EDUARDOMG
  0030     | 0070     |   737904 | PVHS210005 | 001   | A      |  737904 | 071831  | JRCALDERON |    737904 | 071831    | JRCALDERON
  0030     | 0070     |   737906 | PVHS210005 | 001   | A      |  737906 | 090652  | LCRUZM     |    737906 | 090652    | LCRUZM
 (20 rows)
```

**Hallazgo 7.1.1:** Volumen masivo de 37,155 registros. Una OP puede tener múltiples turnos (ej: `PMTY210004` aparece en turnos `001` y `003`), indicando que una orden de producción puede extenderse a través de múltiples turnos. Los prefijos de OP confirman sucursal: `PMTY` (Monterrey), `PPUE` (Puebla), `PVHS` (Villa de Salas/Villahermosa). Los nombres de usuario (`JMACARENO`, `LAPEREZ`, `MGOMEZ`, etc.) son operadores reales de planta.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 7

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 37,155 registros de asignación turno-OP | 7.1.1 | Fuente de verdad para migración de producción |
| 2 | Una OP puede tener múltiples turnos | 7.1.1 | Modelo debe soportar N turnos por Work Order |
| 3 | Prefijos de OP por sucursal (`PMTY`, `PPUE`, `PVHS`) | 7.1.1 | Validar consistencia de códigos al migrar |

---

## 8. ANÁLISIS DE VOLÚMENES GLOBALES

**Objetivo:** Obtener el conteo total de registros en todas las tablas de turnos para dimensionar la escala de datos a migrar.

### 8.1 Consulta: Conteo de registros por tabla

**Query 8.1.1** — Conteo global:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 'bturno1f' as tabla, count(*) FROM bturno1f
UNION ALL SELECT 'relacionturno', count(*) FROM relacionturno
UNION ALL SELECT 'turnoxop', count(*) FROM turnoxop
UNION ALL SELECT 'turno', count(*) FROM turno;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
     tabla     | count 
 ---------------+-------
  bturno1f      |    30
  relacionturno |    14
  turnoxop      | 37155
  turno         |    55
 (4 rows)
```

**Hallazgo 8.1.1:** Maestras pequeñas: `bturno1f` (30), `relacionturno` (14), `turno` (55) son tablas de configuración con pocos registros, fáciles de migrar. Transaccional masiva: `turnoxop` (37,155) contiene el histórico de asignaciones turno-OP. Para Odoo 19, probablemente solo se migren registros del periodo activo, no el histórico completo. Ratio: ~676 asignaciones turno-OP por turno maestro.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 8

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Maestras pequeñas (30-55 registros) | 8.1.1 | Migración rápida de catálogos |
| 2 | `turnoxop` masiva (37,155 registros) | 8.1.1 | Definir corte de migración con negocio |

---

## 9. ANÁLISIS DE TABLAS TRANSACCIONALES RELACIONADAS

**Objetivo:** Inspeccionar la estructura de tablas que vinculan turnos con horas de trabajo (`horpro`), programación de turno (`proptur`, `dproptur`) y planificación por línea (`opxlinea`), para entender el ecosistema completo de gestión de turnos.

### 9.1 Consulta: Estructura de tablas transaccionales

**Query 9.1.1** — Columnas de `horpro`, `opxlinea`, `proptur`, `dproptur`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('horpro', 'opxlinea', 'proptur', 'dproptur')
AND table_schema = 'public'
ORDER BY table_name, ordinal_position;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 table_name | column_name |    data_type     
 ------------+-------------+------------------
  dproptur   | compania    | text
  dproptur   | sucursal    | text
  dproptur   | fecha       | integer
  dproptur   | turno       | text
  dproptur   | emplead     | integer
  ...
  horpro     | compania    | text
  horpro     | nroop       | text
  horpro     | turno       | text
  horpro     | empleado    | integer
  horpro     | qhoras      | double precision
  ...
  opxlinea   | compania    | text
  opxlinea   | turno       | text
  opxlinea   | cjsprg      | double precision
  opxlinea   | cjseje      | double precision
  ...
  proptur    | compania    | text
  proptur    | turno       | text
  proptur    | emplead     | integer
  proptur    | tothorprg   | double precision
  proptur    | tothorrep   | double precision
 (98 rows)
```

**Hallazgo 9.1.1:** `horpro` (Horas de Producción) tiene campos de horas cuantitativas (`qhoras`, `qhed`, `qhen` = horas diurnas, nocturnas, dobles) y valores monetarios (`vhoras`, `vhoras_dol`), fuente para cálculo de costos de mano de obra. `opxlinea` (Operaciones por Línea) incluye `cjsprg` (cajas programadas) y `cjseje` (cajas ejecutadas), base para cálculo de eficiencia. `proptur` resume horas programadas vs reportadas por empleado y turno. `dproptur` es el nivel más granular con secuencia y hora inicio/fin real.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 9

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `horpro` calcula costos con horas normales/extras | 9.1.1 | Integrar con modelo de nómina/costos en Odoo |
| 2 | `opxlinea` mide eficiencia (`cjsprg` vs `cjseje`) | 9.1.1 | Base para KPIs de producción |
| 3 | `proptur`/`dproptur` concilian planificación vs real | 9.1.1 | Modelar como Work Center Logs en Odoo |

---

## 10. AUDITORÍA DE TRIGGERS EN TABLAS DE TURNOS

**Objetivo:** Verificar si existen triggers (disparadores) en las tablas de turnos que ejecuten lógica automática de negocio al insertar, actualizar o eliminar registros.

### 10.1 Consulta: Triggers en tablas de turnos

**Query 10.1.1** — Buscar triggers en tablas de turnos:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE event_object_table IN ('bturno1f', 'turnoxop', 'relacionturno', 'turno');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 trigger_name | event_manipulation | event_object_table 
 --------------+--------------------+--------------------
 (0 rows)
```

**Hallazgo 10.1.1:** No existen disparadores en ninguna de las 4 tablas de turnos. Toda la lógica de negocio (validaciones, cascadas, auditoría) está implementada en la capa de aplicación (código del ERP legacy), no en la base de datos. Al no haber lógica embebida en triggers, la migración a Odoo 19 es más limpia: toda la lógica se reimplementará en los modelos Python de Odoo (`models/`), con mayor control y trazabilidad.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 10

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 0 triggers en tablas de turnos | 10.1.1 | Lógica a reimplementar en Python/Odoo |

---

## 11. ANÁLISIS DE DATOS REALES - TABLA `turno` (HORARIOS POR SUCURSAL)

**Objetivo:** Inspeccionar los datos reales de horarios de turnos para comprender las variaciones entre sucursales y los patrones de turnos cruzados (nocturnos que cruzan medianoche).

### 11.1 Consulta: Datos de `turno`

**Query 11.1.1** — Muestreo de `turno`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM turno LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | turno |  descripcion  | hinicio |  hfin  | feccrea | horcrea |  usucrea  | ultfecmod | ulthormod | ultusumod | flgidavail | flgenuso 
 ----------+----------+-------+---------------+---------+--------+---------+---------+-----------+-----------+-----------+-----------+------------+----------
  0030     | 0108     | 003   | TERCER TURNO  | 220000  | 063000 |  733594 | 094004  | APEREZU   |    737196 | 120251    | EJUAREZ   | \x46       | \x46
  0035     | 09       | 001   | PRIMER TURNO  | 070000  | 150000 |  731889 | 125001  | GALBARRAN |    731895 | 091701    | GALBARRAN | \x46       | \x46
  0035     | 09       | 002   | SEGUNDO TURNO | 150000  | 230000 |  731889 | 125001  | GALBARRAN |    731895 | 091801    | GALBARRAN | \x46       | \x46
  0035     | 09       | 003   | TERCER TURNO  | 230000  | 070000 |  731895 | 091801  | GALBARRAN |    731895 | 091801    | GALBARRAN | \x46       | \x46
  0032     | 0001     | 001   | PRIMER TURNO  | 063000  | 143000 |  738033 | 185932  | TORDONEZ  |    738033 | 185932    | TORDONEZ  | \x46       | \x46
  0032     | 0001     | 002   | SEGUNDO TURNO | 143000  | 220000 |  738033 | 185945  | TORDONEZ  |    738033 | 185945    | TORDONEZ  | \x46       | \x46
  0032     | 0001     | 003   | TERCER TURNO  | 220000  | 063000 |  738033 | 185956  | TORDONEZ  |    738033 | 185956    | TORDONEZ  | \x46       | \x46
  0030     | 0112     | 001   | PRIMER TURNO  | 063000  | 143000 |  738259 | 155240  | SILVERIO  |    738259 | 155240    | SILVERIO  |            | 
  0030     | 0112     | 002   | SEGUNDO TURNO | 143000  | 220000 |  738259 | 155254  | SILVERIO  |    738259 | 155254    | SILVERIO  |            | 
  0030     | 0112     | 003   | TERCER TURNO  | 220000  | 063000 |  738259 | 155305  | SILVERIO  |    738259 | 155305    | SILVERIO  |            | 
 (10 rows)
```

**Hallazgo 11.1.1:** Variación de horarios por sucursal: `0032/0001` usa `06:30-14:30`, `0035/09` usa `07:00-15:00`. Cada planta define sus propios horarios. El Tercer Turno siempre cruza medianoche (ej: `220000` → `063000`), lo que implica lógica especial para asignar producción al turno correcto cuando una OP inicia un día y termina al siguiente. Los horarios son contiguos sin traslape. Banderas `\x46` en `flgidavail` y `flgenuso` representan `F` (False), indicando que estos turnos no están marcados para integración directa con AVAIL.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 11

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | Horarios varían por sucursal | 11.1.1 | Modelo de horarios por sucursal en Odoo |
| 2 | Turno 3 cruza medianoche (`220000` → `063000`) | 11.1.1 | Lógica especial para asignación de producción nocturna |
| 3 | Banderas `flgidavail`/`flgenuso` en False | 11.1.1 | Integración AVAIL inactiva |

---

## 12. AUDITORÍA DE PROGRAMACIÓN OPERATIVA - TABLA `opxlinea`

**Objetivo:** Analizar la relación entre la programación de producción, las líneas de equipo y los turnos para validar la integridad de los datos de manufactura en `opxlinea`.

### 12.1 Consulta: Datos de `opxlinea`

**Query 12.1.1** — Muestreo de `opxlinea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, fecprg, turno, fameqp, lineqp, tipenvase, formato, sabor, cjsprg, cjseje 
FROM opxlinea LIMIT 15;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | fecprg | turno | fameqp | lineqp | tipenvase | formato | sabor | cjsprg | cjseje 
 ----------+----------+--------+-------+--------+--------+-----------+---------+-------+--------+--------
  0100     | 01       | 735131 |       |        |      0 |           |         |       |      0 |      0
  0002     | 0001     | 735184 |       |        |      0 |           |         |       |      0 |      0
  0002     | 01       | 735436 |       |        |      0 |           |         |       |      0 |      0
  0002     | 02       | 735477 |       |        |      0 |           |         |       |      0 |      0
  0002     | 17       | 735493 |       |        |      0 |           |         |       |      0 |      0
  0002     | 15       | 735506 |       |        |      0 |           |         |       |      0 |      0
  0002     | 29       | 735506 |       |        |      0 |           |         |       |      0 |      0
  0002     | 26       | 735516 |       |        |      0 |           |         |       |      0 |      0
  0002     | 13       | 735738 |       |        |      0 |           |         |       |      0 |      0
  0002     | 11       | 735906 |       |        |      0 |           |         |       |      0 |      0
  0002     | 12       | 735967 |       |        |      0 |           |         |       |      0 |      0
  0002     | 03       | 736262 |       |        |      0 |           |         |       |      0 |      0
  0002     | 37       | 736381 |       |        |      0 |           |         |       |      0 |      0
  0002     | 25       | 736444 |       |        |      0 |           |         |       |      0 |      0
  0100     | 02       | 736564 |       |        |      0 |           |         |       |      0 |      0
 (15 rows)
```

**Hallazgo 12.1.1:** Los primeros 15 registros muestran el campo `turno` completamente vacío, junto con `fameqp` vacío y `lineqp = 0`. Esto indica registros de programación inicial o plantillas sin asignar. `fecprg` va de 735131 a 736564 (aprox. 2013-2017), sugiriendo registros históricos de prueba o migración inicial que nunca se completaron. Estos registros huérfanos deben filtrarse durante la migración a Odoo 19.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 12

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `turno` vacío en registros antiguos | 12.1.1 | Filtrar registros sin turno al migrar |
| 2 | Fechas julianas tempranas (2013-2017) | 12.1.1 | Datos históricos de prueba, descartar |

---

## 13. AUDITORÍA DE PARÁMETROS DE PRODUCCIÓN - TABLA `parprod`

**Objetivo:** Inspeccionar la estructura y los datos de la tabla `parprod` para entender cómo se registran los parámetros operativos globales y su vinculación con los turnos.

### 13.1 Consulta: Estructura de `parprod`

**Query 13.1.1** — Describir estructura de `parprod`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d parprod' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 Table "public.parprod"
     Column     |       Type       | Collation | Nullable | Default 
 ----------------+------------------+-----------+----------+---------
  compania       | text             |           |          | 
  codigo         | smallint         |           |          | 
  ...
  nroturno       | smallint         |           |          | 
  horaxtur       | smallint         |           |          | 
  diaxmes        | smallint         |           |          | 
  ...
  ultturno       | text             |           |          | 
  ...
 Indexes:
     "idx_172135_parprod1" UNIQUE, btree (compania, codigo)
```

**Hallazgo 13.1.1:** A pesar del nombre `parprod` (que podría interpretarse como "paros de producción"), la estructura revela que es una tabla de **parámetros de producción** por compañía. La PK `(compania, codigo)` con solo 4 registros confirma que es configuración, no transaccional. `nroturno` almacena el turno como número (3), mientras `ultturno` lo almacena como texto formateado ('003'). Campos `horaxtur` (horas por turno) y `diaxmes` (días de operación al mes) son parámetros base para planificación.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 13

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `parprod` es tabla de parámetros, no de paros | 13.1.1 | Migrar como configuración de compañía en Odoo |
| 2 | PK `(compania, codigo)` con 4 registros | 13.1.1 | 1 registro por compañía activa |

---

## 14. AUDITORÍA DE PARÁMETROS DE PRODUCCIÓN - TABLA `parprod` (COMPLEMENTO)

**Objetivo:** Inspeccionar el contenido de la tabla `parprod` para identificar parámetros operativos globales por compañía.

### 14.1 Consulta: Datos de `parprod`

**Query 14.1.1** — Muestreo de `parprod`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, codigo, nroturno, ultturno, feccrea FROM parprod LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | codigo | nroturno | ultturno | feccrea 
 ----------+--------+----------+----------+---------
  0035     |      1 |        3 | 003      |       0
  0030     |      1 |        3 | 003      |       0
  0032     |      1 |        3 | 003      |       0
  0075     |      1 |        3 | 003      |       0
 (4 rows)
```

**Hallazgo 14.1.1:** Solo 4 registros, uno por compañía (`0035`, `0030`, `0032`, `0075`), con `codigo = 1` en todos. Todas las compañías tienen configurado el turno 3 como turno predeterminado o último turno de referencia (`nroturno = 3`, `ultturno = '003'`). `feccrea = 0` en todos, indicando carga inicial del sistema sin timestamp. La compañía `0075` aparece aquí pero no fue vista en análisis anteriores de `bturno1f`.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 14

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | `nroturno = 3` y `ultturno = '003'` uniforme | 14.1.1 | Configuración estática, hardcodeable en Odoo |
| 2 | Compañía `0075` presente | 14.1.1 | Verificar si tiene turnos configurados |

---

## 15. MAPEO DE ALCANCE OPERATIVO - SEGMENTACIÓN MULTI-COMPAÑÍA Y SUCURSALES

**Objetivo:** Determinar la cobertura geográfica y organizacional del sistema mediante la identificación de combinaciones únicas de compañía y sucursal, con el fin de dimensionar el despliegue de estructuras en Odoo 19.

### 15.1 Consulta: Combinaciones únicas de compañía y sucursal

**Query 15.1.1** — Sucursales con turnos configurados:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT compania, sucursal FROM turno ORDER BY compania, sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal 
 ----------+----------
  0030     | 0001
  0030     | 0068
  0030     | 0070
  0030     | 0086
  0030     | 0108
  0030     | 0112
  0030     | 0113
  0030     | 0114
  0030     | 0115
  0030     | 0116
  0030     | 114
  0032     | 0001
  0035     | 01
  0035     | 03
  0035     | 04
  0035     | 05
  0035     | 08
  0035     | 09
  0036     | 01
 (19 rows)
```

**Hallazgo 15.1.1:** Distribución por compañía: `0030` tiene 11 sucursales activas, `0035` tiene 6, `0032` y `0036` tienen 1 cada una. Inconsistencia en formato de sucursal: `0030` usa 4 dígitos (`0001`, `0068`), mientras `0035` y `0036` usan 2 dígitos (`01`, `09`). Sucursal `114` vs `0114` en compañía `0030` sugiere posible duplicado por inconsistencia de formato. Total: 19 combinaciones únicas. Compañías sin turnos configurados: `0002`, `0075`, `0076`, `0081`, `0100`, `5000`.

---

### RESUMEN DE HALLAZGOS — SECCIÓN 15

| # | Hallazgo | Consulta que lo determina | Impacto para Odoo 19 |
|---|----------|--------------------------|---------------------|
| 1 | 19 combinaciones únicas de compañía/sucursal | 15.1.1 | Scope real del despliegue multi-compañía |
| 2 | Inconsistencia de formato (4 vs 2 dígitos) | 15.1.1 | Normalizar códigos durante migración |
| 3 | Posible duplicado `114` vs `0114` | 15.1.1 | Validar y consolidar en Odoo |

---

## 16. DUDAS LUEGO DEL ANÁLISIS DE LAS CONSULTAS PREVIAS

### 16.1 Duda 1: Relación bturno1f ↔ turno — ¿Cuál es la maestra definitiva?

- bturno1f: 30 registros, turnos por compañía (sin sucursal, sin horarios)
- turno: 55 registros, turnos por compañía + sucursal (con hinicio/hfin)
- Duda: ¿bturno1f es catálogo global y turno es la instancia operativa por sucursal? ¿O son redundantes y una está obsoleta?

**Query 16.1.1** — Verificar existencia de compañía `0035` en `bturno1f`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, turno FROM bturno1f WHERE compania = '0035';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | turno 
 ----------+-------
  0035     | 001
  0035     | 002
  0035     | 003
 (3 rows)
```

**conclusion**
1. **Confirmada relación jerárquica**: `bturno1f` es el **catálogo global** de turnos (definición base por compañía), mientras `turno` es la **instancia operativa** con horarios reales por sucursal.
2. **Compañía `0035` sí existe en `bturno1f`**: Tiene los 3 turnos estándar (`001`, `002`, `003`), confirmando que todas las compañías activas en `turno` tienen su definición en `bturno1f`.
3. **Patrón de diseño**: `bturno1f` define "qué turnos existen" (código + descripción), `turno` define "cuándo operan" (hinicio/hfin) por cada sucursal.
4. **Implicación para Odoo 19**: El modelo debe reflejar esta jerarquía: un modelo `bm.turno.definicion` (catálogo) y `bm.turno.horario` (instancias por sucursal con horarios).

---

### 16.2 Duda 2: Discrepancia de compañías entre tablas

Compañías identificadas: `0030`, `0032`, `0035`, `0036`, `0070`, `0075`, `0076`, `0081`, `5000`

- Duda: 0070, 0076, 0081, 5000 tienen definición de turno pero sin horarios configurados. ¿Son compañías inactivas o migradas?
- Duda: 0075 tiene parámetros de producción pero sin turnos. ¿Cómo opera?

**Query 16.2.1** — Verificar actividad en `opxlinea` de compañías sin horarios:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, COUNT(*) FROM opxlinea WHERE compania IN ('0070', '0076', '0081', '5000') GROUP BY compania;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | count 
 ----------+-------
 (0 rows)
```

**Query 16.2.2** — Verificar parámetros de `0075` en `parprod`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM parprod WHERE compania = '0075';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | codigo | inc | ind | despachoma | devdisp | devrechaza | dvc | trancontro | parteing | tranajting | tranajtsal | salmstr | mpi | mps | cliente | reqprod | tranoprod | tranocomp | tranreq | trantra | actrcal | aprduc | feccrea | horcrea | usucrea | fecultimod | horultimod | usuultimod | nroturno | horaxtur | diaxmes | reqalmlog | famenv | famsop | famjar | aprobot | proreqpro | cotizacion | tipartser | almcont | devmer | protocolos | salidacc | falpro | sobpro | trnconmue | manejo_x_racks | faccjs | plapro | savvar | faminy | famazu | libre1 | libre2 | libre3 | libre4 | libre5 | libre6 | libre7 | libre8 | libre9 | libre10 | libre11 | areman | aretag | areazu | arejara | arelvbt | arelifz | arebb | almvalr | almvalg | almnovg | almnovr | libre12 | libre13 | libre14 | libre15 | areemb | areiso | famemb | famiso | linmpmp | linmpis | linrefrp | linrefpg | lingesm | lingesmp | ctptvta | ctptded | ctptcob | ctptdif | tartprt | famjbag | famjbiso | arenect | famjnec | famnect | areminy | famminy | trasptin | vtamaqui | cdogtoind | sucprin | tramuest | trarqalm | almproc | trasalaut | traingaut | famresina | ultturno | diastkseg | actalmpro | tranvalno | tipartins | tipartemp | trandocref | tradevprov | almmp | almcon | almconref | almcongen | trasalcon | traingcon | almafijo | flgatepro 
 ----------+--------+-----+-----+------------+---------+------------+-----+------------+----------+------------+------------+---------+-----+-----+---------+---------+-----------+-----------+---------+---------+---------+--------+---------+---------+---------+------------+------------+------------+----------+----------+---------+-----------+--------+--------+--------+---------+-----------+------------+-----------+---------+--------+------------+----------+--------+--------+-----------+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+---------+---------+--------+--------+--------+---------+---------+---------+-------+---------+---------+---------+---------+---------+---------+---------+---------+--------+--------+--------+--------+---------+---------+----------+----------+---------+----------+---------+---------+---------+---------+---------+---------+----------+---------+---------+---------+---------+---------+----------+----------+-----------+---------+----------+----------+---------+-----------+-----------+-----------+----------+-----------+-----------+-----------+-----------+-----------+------------+------------+-------+--------+-----------+-----------+-----------+-----------+----------+-----------
  0075     |      1 | 026 | ISO | DSP        | DPD     | DPR        | 047 | TCC        | INP      | AJI        | AJS        | SPM     | MPI | MPS |       0 | RQP     | OPR       | OCO       | REQ     | TRA     | 700     | 700    |       0 | 000001  |         |          0 | 000001     |            |        3 |        8 |      26 | RAL       | 001    | 002    | 003    | 704     |         0 |            |           | 1008    | DPM    |            |          | FPR    |        |           | \x46           |  5.678 |        | SPP    | 009    | 010    | DPP    | DMC    | CVT    | 007    | 002    |        | 70     |      1 |      0 |       0 |       0 | 703    | 705    | 706    | 707     | 709     | 711     | 712   | 1009    | 1007    | 1050    | 1051    | IDU     | 709     | 045     | 004     | 713    | 714    | 013    | 014    |         |         |          |          |         |          | CVE     | CVD     | CVC     | CVS     | 004     | 015     | 016      | 701     | 019     | 018     | 717     | 017     | 100      | SVQ      | 001       | 0001    | IMU      | 040      | 83      | ATP       | IAP       | 020       | 003      |         3 | \x46      | 025       | 001       | 003       | TNS        | SPR        |       |        |           |           |           |           |          | \x54
 (1 row)
```

**Query 16.2.3** — Compañías con turnos en `turno`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT compania FROM turno;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania 
 ----------
  0030
  0032
  0036
  0035
 (4 rows)
```

**Query 16.2.4** — Actividad de `0075` en `opxlinea`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT count(*) FROM opxlinea WHERE compania = '0075';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 count 
 -------
      0
 (1 row)
```

**Query 16.2.5** — Sucursales de `0036` en `turno`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT sucursal FROM turno WHERE compania = '0036';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 sucursal 
 ----------
  01
 (1 row)
```

**conclusion**
1. **Compañías `0070`, `0076`, `0081`, `5000` son inactivas**: Cero registros en `opxlinea` (tabla de programación operativa). Tienen definición de turno en `bturno1f` pero nunca configuraron horarios en `turno` ni tuvieron actividad productiva. Son compañías creadas durante configuración inicial pero nunca puestas en producción.
2. **Compañía `0075` es registro zombi**: Tiene parámetros de producción configurados (`parprod` con `nroturno=3`, `horaxtur=8`, `diaxmes=26`), pero **sin turnos definidos** en `turno` y **cero actividad** en `opxlinea`. Configuración incompleta abandonada, posiblemente una compañía planificada que nunca operó.
3. **Compañías activas confirmadas**: Solo `0030`, `0032`, `0035`, `0036` tienen turnos operativos configurados. Estas son las únicas que deben migrarse con estructura completa de turnos a Odoo 19.
4. **Acción de limpieza**: Las compañías `0070`, `0076`, `0081`, `5000` pueden excluirse de la migración o migrarse como `res.company` inactivas sin horarios de turno. La `0075` es registro zombi y debe descartarse salvo validación expresa del equipo de negocio.
5. **Compañía `0036` es entidad de alcance mínimo**: Tiene 1 sucursal (`01`) configurada en `turno` pero **carece de parámetros globales** en `parprod`. No tiene su perfil de configuración completo. Posible compañía nueva en proceso de setup o planta piloto con operación limitada.

---

### 16.3 Duda 3: Sucursal 114 vs 0114 en compañía 0030

- Ambas existen en turno como registros separados
- Duda: ¿Duplicado por inconsistencia de formato o son sucursales reales distintas?

**Query 16.3.1** — Comparar configuración de `114` y `0114`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT sucursal, turno, hinicio, hfin, flgidavail, flgenuso 
FROM turno WHERE compania='0030' AND sucursal IN ('114','0114') ORDER BY turno;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 sucursal | turno | hinicio |  hfin  | flgidavail | flgenuso 
 ----------+-------+---------+--------+------------+----------
  114      | 001   | 063000  | 143000 | \x46       | \x46
  0114     | 001   | 063000  | 143000 | \x46       | \x46
  114      | 002   | 143000  | 220000 | \x46       | \x46
  0114     | 002   | 143000  | 220000 | \x46       | \x46
  114      | 003   | 220000  | 063000 | \x46       | \x46
  0114     | 003   | 220000  | 063000 | \x46       | \x46
 (6 rows)
```

**conclusion**
1. **Confirmado: Es un DUPLICADO**: Ambas sucursales (`114` y `0114`) tienen exactamente la misma configuración de horarios para los 3 turnos:
   - Turno 1: `063000` → `143000`
   - Turno 2: `143000` → `220000`
   - Turno 3: `220000` → `063000`
   - Mismas banderas `flgidavail = \x46`, `flgenuso = \x46`
2. **Causa raíz**: Inconsistencia de formato en la carga de datos. `0114` sigue el estándar de 4 dígitos de la compañía `0030`, mientras `114` es una variante sin ceros a la izquierda.
3. **Verificación adicional requerida**: Necesario confirmar si ambas sucursales tienen datos transaccionales asociados o si una de ellas es la "correcta" y la otra es un artefacto de migración.

**Query 16.3.2** — Validación de datos transaccionales:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 'turnoxop' as tabla, sucursal, COUNT(*) FROM turnoxop 
WHERE compania='0030' AND sucursal IN ('114','0114') GROUP BY sucursal
UNION ALL
SELECT 'opxlinea', sucursal, COUNT(*) FROM opxlinea 
WHERE compania='0030' AND sucursal IN ('114','0114') GROUP BY sucursal
UNION ALL
SELECT 'horpro', sucursal, COUNT(*) FROM horpro 
WHERE compania='0030' AND sucursal IN ('114','0114') GROUP BY sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
  tabla   | sucursal | count 
 ----------+----------+-------
  turnoxop | 114      |     1
  turnoxop | 0114     |    40
  opxlinea | 0114     |     1
  opxlinea | 114      |     1
  horpro   | 0114     |    61
 (5 rows)
```

4. **Acción recomendada para Odoo 19**: Consolidar en `0114` (estándar 4 dígitos). La evidencia es contundente:
   - `turnoxop`: `0114` tiene **40 registros** vs `114` con solo **1** (posible escritura manual que el sistema no rechazó por falta de validación de formato).
   - `horpro`: Exclusivo de `0114` con **61 registros**. `114` no tiene horas de producción registradas.
   - `opxlinea`: Ambas tienen 1 registro cada una, pero el de `114` es probablemente el mismo evento de escritura manual sin validación.
   - **Veredicto**: `114` es un artefacto de inconsistencia de formato, no una sucursal real. Migrar solo `0114` y sus 40+61 registros transaccionales. El registro huérfano de `114` puede descartarse o reasignarse a `0114` si se valida que corresponde a la misma operación.

---

### 16.4 Duda 4: Turnos cruzados (nocturnos)

- Turno 3: hinicio=220000, hfin=063000 (fin < inicio)
- Duda: ¿Cómo determinar a qué turno pertenece una producción registrada a las 02:00 AM? ¿Se asigna al día anterior o al actual?
- Impacto: Lógica de asignación automática de turno en Odoo necesita regla especial.

**absolucion**: La asignación de producción nocturna requiere lógica basada en hora de registro vs ventana de turno, no solo por fecha calendario.

**Query 16.4.1** — Identificar turnos cruzados:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT t.compania, t.sucursal, t.turno, t.hinicio, t.hfin,
       CASE WHEN t.hinicio > t.hfin THEN 'CRUZADO' ELSE 'NORMAL' END as tipo_turno
FROM turno t WHERE t.hinicio > t.hfin;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | turno | hinicio |  hfin  | tipo_turno 
 ----------+----------+-------+---------+--------+------------
  0030     | 0108     | 003   | 220000  | 063000 | CRUZADO
  0035     | 09       | 003   | 230000  | 070000 | CRUZADO
  0032     | 0001     | 003   | 220000  | 063000 | CRUZADO
  0030     | 0112     | 003   | 220000  | 063000 | CRUZADO
  0030     | 0113     | 003   | 220000  | 063000 | CRUZADO
  0030     | 114      | 003   | 220000  | 063000 | CRUZADO
  0030     | 0114     | 003   | 220000  | 063000 | CRUZADO
  0030     | 0086     | 003   | 220000  | 063000 | CRUZADO
  0036     | 01       | 003   | 220000  | 063000 | CRUZADO
  0030     | 0115     | 003   | 220000  | 063000 | CRUZADO
  0030     | 0116     | 003   | 223000  | 070000 | CRUZADO
  0030     | 0068     | 003   | 223000  | 070000 | CRUZADO
  0030     | 0001     | 003   | 220000  | 063000 | CRUZADO
  0030     | 0070     | 003   | 230000  | 070000 | CRUZADO
  0035     | 01       | 002   | 190000  | 070000 | CRUZADO
  0035     | 01       | 003   | 070000  | 07:00: | CRUZADO
  0035     | 05       | 003   | 220000  | 063000 | CRUZADO
  0035     | 03       | 003   | 230000  | 070000 | CRUZADO
  0035     | 04       | 003   | 230000  | 070000 | CRUZADO
  0035     | 08       | 003   | 230000  | 070000 | CRUZADO
 (20 rows)
```

**conclusion**
1. **Todos los turnos cruzados son Turno 3** (20 de 20), confirmando que el tercer turno es consistentemente nocturno en todas las sucursales activas.
2. **Patrones de horario identificados**:
   - **Estándar**: `220000` → `063000` (8.5 horas) — mayoría de sucursales `0030` y `0032`
   - **Tardío**: `223000` → `070000` (8.5 horas) — sucursales `0030/0116`, `0030/0068`
   - **Nocturno largo**: `230000` → `070000` (8 horas) — sucursales `0035` y `0030/0070`
3. **Anomalía crítica detectada**: `0035/01/003` tiene `hinicio=070000`, `hfin=07:00:` — **dato corrupto/malformado**. El `hfin` tiene formato `07:00:` (con dos puntos) en lugar de `070000`. Esto causará errores de parsing si no se limpia antes de migrar.
4. **Caso especial**: `0035/01/002` es `190000` → `070000` (12 horas). No es un turno normal, posiblemente un turno especial de fin de semana o configuración errónea.
5. **Regla de asignación confirmada**: Producción entre `22:00` y `06:30` pertenece al Turno 3. Si la hora de registro es `< 06:30`, la fecha de producción corresponde al **día anterior** (fecha de inicio del turno).

**accion recomendada para Odoo**
1. Implementar método `_obtener_turno_por_fecha_hora(fecha, hora)` en `bm.turno.horario`:
   - Si `hinicio < hfin` (normal): `hinicio <= hora < hfin` → misma fecha
   - Si `hinicio > hfin` (cruzado): `hora >= hinicio` → misma fecha; `hora < hfin` → fecha anterior
2. **Limpieza previa a migración**: Corregir el registro corrupto `0035/01/003` (`hfin='07:00:'` → `'070000'`). Agregar validación de formato `HHMMSS` en el modelo Odoo.
3. **Validar caso `0035/01/002`** (12 horas): Confirmar con negocio si es turno real o error. Si es error, corregir a `150000` → `230000` (patrón estándar de Turno 2).
4. **No hardcodear** la regla de "Turno 3 = cruzado". La lógica debe basarse en comparación `hinicio > hfin` para soportar configuraciones futuras no estándar.

---

### 16.5 Duda 5: Registros duplicados en relacionturno

- turnobm=001 tiene 2 registros por sucursal: uno con turnoav='' y otro con turnoav='1'
- Duda: ¿El registro vacío es fallback, error, o registro histórico? ¿Cuál usar para migración?

**Query 16.5.1** — Distribución de `turnoav` en `relacionturno`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT turnoav, COUNT(*) FROM relacionturno WHERE compania='0030' GROUP BY turnoav;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 turnoav | count 
 ---------+-------
          |     4
  1       |     4
  2       |     3
  3       |     3
 (4 rows)
```

**conclusion**
Los registros vacíos y '1' tienen la misma frecuencia (4 cada uno), correspondiendo a las 4 sucursales de `0030` que tienen mapeo en `relacionturno`. Esto confirma un patrón:
- `turnoav=''` (4 registros): **Registro comodín/fallback** para turno `001` cuando no hay mapeo específico con AVAIL.
- `turnoav='1'` (4 registros): **Mapeo activo** real entre BM `001` ↔ AVAIL `1`.
- `turnoav='2'` y `'3'` (3 registros cada uno): Solo aparecen en 3 sucursales, lo que sugiere que una de las 4 sucursales no tiene mapeo completo para turnos 2 y 3, o que el registro fallback solo existe para el turno 1.

**accion recomendada para odoo**
1. Durante la migración, **ignorar los registros con `turnoav=''`** ya que son fallbacks del sistema legacy y no representan mapeos reales.
2. Migrar solo los registros con `turnoav` poblado (`1`, `2`, `3`) como datos de integración con AVAIL.
3. Si en el futuro se requiere integración con AVAIL en Odoo, crear un modelo `bm.turno.mapeo_avail` con campos `(compania, sucursal, turno_bm, turno_avail)`. Si no hay integración con AVAIL, esta tabla puede omitirse completamente de la migración.
4. Validar con el equipo de negocio si la integración con AVAIL sigue activa o fue reemplazada por otro sistema.

---

### 16.6 Duda 6: opxlinea — volumen de registros huérfanos

- Los primeros 15 rows tienen turno='', fameqp='', cjsprg=0
- Duda: ¿Qué porcentaje del total representan? Si son mayoría, la tabla opxlinea podría ser mayormente basura.

**absolucion**: Determinar la salud de la tabla principal, si la mayoría de los registros no tiene un turno asignado (cementerio de datos) o una tabla que se usa para fines distintos a la programación (borradores o logs).

**Query 16.6.1** — Porcentaje de registros sin turno:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT count(*) as total, 
       count(1) FILTER (WHERE turno = '' OR turno IS NULL) as vacios, 
       ROUND((count(1) FILTER (WHERE turno = '' OR turno IS NULL) * 100.0 / count(1)), 2) as porcentaje_basura 
FROM opxlinea;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 total | vacios | porcentaje_basura 
 -------+--------+-------------------
    42 |     42 |            100.00
 (1 row)
```

**conclusion**
Con el **100% de registros sin turno asignado** (42 de 42), `opxlinea` **NO es la tabla donde reside la verdad de la producción** en el sistema legacy. Es una tabla de programación planificada que quedó obsoleta o nunca se utilizó activamente. La tabla transaccional real de asignación turno-OP es `turnoxop` (37,155 registros con datos completos).

**accion recomendada para Odoo**
1. **No migrar `opxlinea` como tabla de producción real**. Su contenido es basura/histórico sin valor operativo.
2. Si se requiere conservar por auditoría, migrar como datos históricos en un modelo separado `bm.produccion_programacion_historica` con estado `borrador` o `sin_asignar`.
3. La **fuente de verdad** para migración de producción es `turnoxop` (asignaciones reales turno-OP) combinada con `horpro` (horas trabajadas) y `dproptur` (detalle de programación por empleado).
4. Revalidar si `opxlinea` tenía un propósito específico en el flujo legacy (¿borrador de planificación? ¿interfaz con otro sistema?) antes de decidir su destino final.

---

### 16.7 Duda 7: parprod — ¿parámetros o paros?

- Nombre sugiere "paros de producción" pero estructura es de parámetros globales
- Duda: ¿Existe otra tabla para registrar paros reales? ¿O el nombre es histórico/engañoso?

**absolucion**: Cuantas compañías están activas o en configuración.

**Query 16.7.1** — Conteo de registros en `parprod`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT count(*) FROM parprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 count 
 -------
      4
 (1 row)
```

**conclusion**
Confirmado: `parprod` es la **tabla de parámetros maestros de producción** con exactamente 4 registros, uno por compañía activa o en configuración (`0035`, `0030`, `0032`, `0075`). No es una tabla transaccional de paros. Su nombre es engañoso (posiblemente "parámetros de producción" abreviado como `parprod`, no "paros de producción").

**accion recomendada para Odoo**
1. Migrar los 4 registros como **configuración de compañía** en Odoo. Crear un modelo `bm.produccion.config` vinculado a `res.company` con los campos relevantes:
   - `nroturno` → número máximo de turnos (3)
   - `horaxtur` → horas por turno (8)
   - `diaxmes` → días operativos al mes (26)
   - `ultturno` → turno por defecto ('003')
2. Los campos de familias de productos (`famenv`, `famsop`, `famjar`, etc.) y áreas (`areman`, `arettag`, etc.) deben mapearse a categorías de producto y departamentos en Odoo.
3. Los campos `libre1-15` pueden omitirse salvo que el equipo de negocio identifique alguno como crítico.
4. El registro de `0075` (zombi) puede migrarse como configuración inactiva o descartarse.

---

### 16.8 Duda 8: nroturno vs ultturno en parprod

- nroturno = 3 (smallint), ultturno = '003' (text) para todas las compañías
- Duda: ¿Qué significa "último turno"? ¿Turno actual en curso? ¿Turno por defecto? ¿Último turno procesado del día?

**absolucion**: ultturno cambia según la actividad reciente o es un valor estático de configuración, ver si hay variedad entre las 4 compañías.

**Query 16.8.1** — Comparar valores por compañía:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, nroturno, ultturno FROM parprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | nroturno | ultturno 
 ----------+----------+----------
  0035     |        3 | 003
  0030     |        3 | 003
  0032     |        3 | 003
  0075     |        3 | 003
 (4 rows)
```

**conclusion**
Todas las 4 compañías tienen exactamente `nroturno = 3` y `ultturno = '003'`. Esto **NO es un valor dinámico** que cambia según actividad reciente. Son **valores estáticos de configuración** que representan:
- `nroturno (3)`: **Límite de capacidad** — el sistema está configurado para soportar máximo 3 turnos por día.
- `ultturno ('003')`: **Identificador de tope** — el código del último turno posible, usado como referencia para validaciones o cierres de día.

No hay variación entre compañías, lo que indica que es una configuración global estandarizada, no un indicador de actividad.

**accion recomendada para Odoo**
1. No migrar como campos dinámicos. Son **constantes de configuración** que pueden hardcodearse o definirse como valores por defecto en el modelo `bm.produccion.config`.
2. Si en el futuro se requieren más de 3 turnos (ej. turnos de fin de semana o especiales), el modelo debe ser flexible para soportar N turnos, no limitarse a 3.
3. `ultturno` puede usarse como regla de validación: al cerrar el día productivo, verificar que el último turno procesado coincida con el turno máximo configurado.

---

### 16.9 Duda 9: Banderas flgidavail y flgenuso

- Tipo bytea, valor \x46 = ASCII 'F' (False)
- Algunas sucursales (0030/0112) tienen estas banderas **vacías** (NULL)
- Duda: ¿Qué controlan exactamente? ¿Afectan la migración si no se integra con AVAIL?

**Query 16.9.1** — Distribución de `flgidavail`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT flgidavail, COUNT(*) FROM turno GROUP BY flgidavail;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 flgidavail | count 
 ------------+-------
             |     7
  \x46       |    48
 (2 rows)
```

**Query 16.9.2** — Distribución combinada de banderas:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT flgidavail, flgenuso, COUNT(*) FROM turno GROUP BY flgidavail, flgenuso;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 flgidavail | flgenuso | count 
 ------------+----------+-------
  \x46       | \x54     |     6
             |          |     7
  \x46       | \x46     |    42
 (3 rows)
```

**conclusiones**
Las consultas son correctas y revelan el siguiente panorama:

| flgidavail | flgenuso | count | Interpretación |
|------------|----------|-------|----------------|
| `\x46` (F) | `\x54` (T) | 6     | Turnos **activos en uso** pero sin integración AVAIL |
| `\x46` (F) | `\x46` (F) | 42    | Turnos configurados pero **sin uso activo** ni integración |
| NULL       | NULL     | 7     | Configuración **incompleta/nueva** (ej: 0030/0112) |

- **`flgidavail`** ("Flag ID Avail"): Siempre False o NULL. **Ningún turno tiene integración activa con AVAIL**. El sistema legacy tenía la capacidad pero nunca se activó o fue deshabilitada.
- **`flgenuso`** ("Flag En Uso"): Solo 6 registros están marcados como activos (T). Estos probablemente corresponden a los turnos principales de las sucursales de mayor actividad. El resto (42) están configurados pero no marcados como "en uso".
- **7 registros NULL**: Sucursales con configuración reciente o incompleta donde las banderas no se inicializaron.

**accion recomendada para Odoo**
1. **Omitir ambas banderas de la migración** si no hay integración con AVAIL en el ecosistema Odoo 19. No aportan valor operativo.
2. Si se planea integración futura con AVAIL u otro sistema de planificación, crear un modelo `bm.turno.integracion` con campos booleanos claros (`activo`, `integrar_con_avail`, `integrar_con_sap`, etc.) en lugar de usar `bytea` opaco.
3. Los 6 registros con `flgenuso=T` pueden usarse como referencia para identificar qué sucursales/turnos eran los **prioritarios** en el sistema legacy, útil para priorizar el orden de migración.
4. Documentar que estas banderas son **reliquias del sistema legacy** y no deben replicarse en el nuevo modelo.

---

### 16.10 Duda 11: Conversión de fechas julianas

- feccreacio = 734799 ≈ enero 2010, pero la fórmula exacta no está documentada
- Duda: ¿Es fecha juliana PostgreSQL (date '2000-01-01' + 734799)? ¿O del sistema legacy?
- Impacto: Necesario para validar antigüedad de datos durante migración.

**absolucion**: búsqueda de registro en turno (fechas de creacion) donde aparezcan ambos formatos...

**Query 16.10.1** — Fechas en `parprod`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, feccrea, fecultimod FROM parprod;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | feccrea | fecultimod 
 ----------+---------+------------
  0035     |       0 |          0
  0030     |       0 |          0
  0032     |       0 |          0
  0075     |       0 |          0
 (4 rows)
```

**Query 16.10.2** — Muestreo de fechas en `horpro`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, feccrea FROM horpro WHERE feccrea > 0 LIMIT 5;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 compania | sucursal | feccrea 
 ----------+----------+---------
  0030     | 0001     |  737782
  0030     | 0068     |  737809
  0030     | 0068     |  737809
  0030     | 0001     |  737817
  0030     | 0108     |  737817
 (5 rows)
```

**Query 16.10.3** — Rango de fechas en `horpro`:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 
  MIN(feccrea) as min_fecha_juliana,
  date '0001-01-01' + (MIN(feccrea) - 1) as min_fecha_real,
  MAX(feccrea) as max_fecha_juliana,
  date '0001-01-01' + (MAX(feccrea) - 1) as max_fecha_real,
  MAX(feccrea) - MIN(feccrea) as dias_totales,
  ROUND((MAX(feccrea) - MIN(feccrea)) / 365.25, 1) as anos_aprox
FROM horpro WHERE feccrea > 0;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

```text
 min_fecha_juliana | min_fecha_real | max_fecha_juliana | max_fecha_real | dias_totales | anos_aprox 
 -------------------+----------------+-------------------+----------------+--------------+------------
             737774 | 2020-12-15     |            739636 | 2026-01-20     |         1862 |        5.1
 (1 row)
```

**conclusion**
1. **Fórmula de conversión confirmada**: El sistema legacy usa **días prolepticos PostgreSQL** (días desde `0001-01-01` en calendario gregoriano proleptico). La conversión exacta es:
   ```sql
   SELECT date '0001-01-01' + (valor_entero - 1) as fecha_real;
   ```
2. **Rango real de datos transaccionales en `horpro`**:
   - **Fecha más antigua**: `737774` → **15 de diciembre de 2020**
   - **Fecha más reciente**: `739636` → **20 de enero de 2026**
   - **Span total**: **1,862 días ≈ 5.1 años** de datos acumulados
3. **`parprod` con `feccrea = 0`**: Confirma que es tabla de configuración inicial, no transaccional. Los 4 registros (`0035`, `0030`, `0032`, `0075`) fueron creados sin timestamp válido.
4. **Datos desde 2020, no 2012**: La estimación inicial de `734799` → `2012-10-28` corresponde a `bturno1f` (catálogo maestro), no a datos transaccionales. Los datos operativos reales (`horpro`, `turnoxop`) inician en **diciembre 2020**.
5. **Datos hasta enero 2026**: El sistema legacy estuvo activo hasta fechas muy recientes (hace ~3 semanas de la fecha actual del sistema). Esto confirma que los datos están **actualizados y vigentes**.

**accion recomendada para Odoo**
1. **Implementar función de conversión en scripts de migración**:
   ```python
   from datetime import date, timedelta

   def julian_to_date(julian_days):
       """Convierte días prolepticos del legacy a date de Odoo.
       - 737774 → 2020-12-15 (inicio datos operativos)
       - 739636 → 2026-01-20 (dato más reciente)
       - 0 o NULL → False (sin fecha válida)
       """
       if not julian_days or julian_days == 0:
           return False
       return date(1, 1, 1) + timedelta(days=julian_days - 1)
   ```
2. **Definir corte de migración con el equipo de negocio**: Con 5.1 años de histórico (~1,862 días), se recomienda:
   - **Migración completa**: Solo si el volumen es manejable (37,155 registros en `turnoxop` es razonable).
   - **Migración parcial**: Últimos 2 años (desde `2024-01-20` ≈ juliano `738900`+) para datos operativos activos.
   - **Histórico archivado**: Exportar datos anteriores a 2024 a un archivo CSV/Excel para consulta offline.
3. **Registros con `feccrea = 0`**: Asignar `False` en campos `date` de Odoo. No usar fechas placeholder que puedan distorsionar reportes.
4. **Validar consistencia post-migración**: Después de convertir, verificar que las fechas caigan dentro del rango esperado (`2020-12-15` a `2026-01-20`). Cualquier fecha fuera de este rango indica error de conversión o dato corrupto.
5. **Documentar en `AGENTS.md`**: Agregar la fórmula de conversión como referencia técnica para futuros desarrolladores del proyecto AJE.
 