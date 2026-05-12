
### SECCIÓN: EXPLORACIÓN DE DICCIONARIO DE DATOS - GESTIÓN DE TURNOS : 
Ejecución de consulta de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas a la gestión de turnos, jornadas y rotaciones dentro del esquema público, con el fin de mapear la estructura de persistencia en `mxbdaje_local`.

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
**Comentario de Hallazgo**:

Se han identificado 4 entidades clave. La tabla bturno1f sigue la nomenclatura de las tablas maestras de configuración (similar a aprfor1f), lo que sugiere que contiene la definición base de los turnos. relacionturno y turnoxop parecen ser tablas de rotación o asignación transaccional (posiblemente vinculando turnos con operaciones o empleados), mientras que turno podría ser una tabla simplificada o una vista remanente. Es necesario inspeccionar bturno1f y turnoxop para entender la lógica de herencia hacia Odoo 19.



### SECCION : Auditoría de Integridad Referencial: Entidad "Turno"
Objetivo
Inspección de todas las columnas del esquema público que contienen referencias a "turno" o "shift" para identificar dependencias en tablas transaccionales, de empleados o de nómina, asegurando el rastreo de la persistencia de jornadas laborales.


```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE (column_name ILIKE '%turno%' OR column_name ILIKE '%shift%') 
AND table_schema = 'public' 
ORDER BY table_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

``` text
table_name       | column_name | data_type 
------------------------+-------------+-----------
 audit02052023ca        | turnodesca  | text
 audit02052023ca        | turnocarga  | text
 audit02052023ca2       | turnocarga  | text
 audit02052023ca2       | turnodesca  | text
 audit27042023ca        | turnocarga  | text
 audit27042023ca        | turnodesca  | text
 av_iapr_result         | shift       | text
 bcnftr1                | nroturno    | smallint
 bcnftr1                | opxturno    | bytea
 bturno1f               | turno       | text
 bturno1f               | descturno1  | text
 bturno1f               | descturno2  | text
 bturno1f               | ststurno    | text
 cabtpro                | turno       | text
 cbarasig               | turno       | text
 ctrlavail              | turno       | text
 detoeetab              | nomturno    | text
 detoeetab              | turno       | text
 dettpro                | turno       | text
 dproptur               | turno       | text
 horpro                 | turno       | text
 ingresados_tcoalm2f_ca | turnocarga  | text
 ingresados_tcoalm2f_ca | turnodesca  | text
 m_prod_hori            | hrsturno    | smallint
 m_prod_prog            | turno       | text
 mequipo1f              | turnos      | integer
 merxlin                | turno       | text
 mpstprgprd1f           | idturno     | integer
 mtiemprod              | turno       | text
 opxlinea               | turno       | text
 orprca                 | turno       | text
 orprpr                 | turno       | text
 orrecab                | turno       | text
 parprod                | nroturno    | smallint
 parprod                | ultturno    | text
 peprod                 | turno       | text
 peprodre               | turno       | text
 planpravail            | turno       | text
 prdxli                 | turno       | text
 prgopdet               | turno       | text
 proptur                | turno       | text
 psprgprod              | turno       | text
 rddtdoc3f              | turno       | text
 relacionturno          | turnoav     | text
 relacionturno          | turnobm     | text
 rpmdevoluciondistrib   | turnodesca  | text
 rpmdevoluciondistrib   | turnocarga  | text
 tcoalm1f               | turnocarga  | text
 tcoalm1f               | turnodesca  | text
 tcodbar1f              | turno       | text
 tcomcam1f              | turnocarga  | text
 tcomcam1f              | turnodesca  | text
 tcomis2f               | turno       | text
 tcomis3f               | turno       | text
 tcomisxf               | turno       | text
 tinvar2                | turno       | text
 tinvarb                | turno       | text
 tinvarcb2              | turno       | text
 tinvciccab             | turno       | text
 tinvcicdet             | turno       | text
 tmpaudit               | turnocarga  | text
 tmpaudit               | turnodesca  | text
 tmpcompcab             | turnoop     | text
 tmptinvar2             | turno       | text
 tordtra1f              | turno       | text
 tparman                | turno       | text
 tplane6                | turno       | smallint
 tproin1                | turnoop     | text
 turno                  | turno       | text
 turnoxop               | turno       | text
 v_prod_plse            | turnoprod   | text
(71 rows)

```

**Comentario de Hallazgo**

El barrido revela una **dispersión masiva** de la entidad "turno" en 71 columnas, confirmando que el sistema maneja la lógica de turnos de forma transversal (Logística, Producción, Auditoría e Inventarios). 

**Puntos Clave**

*   **Tipado de Datos:** La predominancia del tipo `text` sugiere que el sistema no utiliza IDs numéricos secuenciales nativos de Odoo, sino **llaves naturales** mediante códigos (ej. 'T1', 'T2').
*   **Tablas Maestras:** `bturno1f` (Maestra) y `turnoxop` (Operaciones) se perfilan como los puntos de anclaje críticos para la migración hacia los modelos de Odoo 19.
*   **Lógica de Negocio:** La diferenciación entre `turnocarga` y `turnodesca` en tablas de almacén (`tcoalm1f`) indica que los procesos son asíncronos, permitiendo que una operación inicie en un turno y concluya en otro.


## AUDITORÍA TÉCNICA - ENTIDAD: TURNOS (MAESTRAS Y ESTRUCTURA)

### SECCIÓN: EXPLORACIÓN DE DICCIONARIO DE DATOS - GESTIÓN DE TURNOS
**Objetivo**
Ejecución de consulta de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas a la gestión de turnos, jornadas y rotaciones dentro del esquema público, con el fin de mapear la estructura de persistencia en `mxbdaje_local`.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%turno%' OR tablename ILIKE '%turn%' OR tablename ILIKE '%shift%');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
```text
tablename   
---------------
 bturno1f
 relacionturno
 turnoxop
 turno
(4 rows)
```

**Comentario de Hallazgo**
Se han identificado 4 entidades clave. La tabla `bturno1f` sigue la nomenclatura de las tablas maestras de configuración, lo que sugiere que contiene la definición base de los turnos. `relacionturno` y `turnoxop` parecen ser tablas de rotación o asignación transaccional, mientras que `turno` podría ser una tabla simplificada o una vista remanente. Es necesario inspeccionar `bturno1f` y `turnoxop` para entender la lógica de herencia hacia Odoo 19.

---

### SECCIÓN: AUDITORÍA DE INTEGRIDAD REFERENCIAL - CAMPOS DE TURNO
**Objetivo**
Inspección de todas las columnas del esquema público que contienen referencias a "turno" o "shift" para identificar dependencias en tablas transaccionales, de empleados o de nómina, asegurando el rastreo de la persistencia de jornadas laborales.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE (column_name ILIKE '%turno%' OR column_name ILIKE '%shift%') 
AND table_schema = 'public' 
ORDER BY table_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
```text
table_name       | column_name | data_type 
------------------------+-------------+-----------
 audit02052023ca        | turnodesca  | text
 audit02052023ca        | turnocarga  | text
 ... [truncado para brevedad] ...
 bturno1f               | turno       | text
 bturno1f               | descturno1  | text
 tcoalm1f               | turnocarga  | text
 tcoalm1f               | turnodesca  | text
 turnoxop               | turno       | text
(71 rows)
```

**Comentario de Hallazgo**
El barrido revela una **dispersión masiva** de la entidad "turno" en 71 columnas, lo que confirma que el sistema maneja la lógica de turnos de forma transversal. Destaca la predominancia del tipo `text`, sugiriendo el uso de **llaves naturales** (ej. 'T1') en lugar de IDs secuenciales. La diferenciación entre `turnocarga` y `turnodesca` indica procesos asíncronos que inician en un turno y concluyen en otro.

---

### SECCIÓN: ANÁLISIS DE ESTRUCTURA DDL - TABLAS MAESTRAS DE TURNOS
**Objetivo**
Inspeccionar la definición técnica de las tablas `bturno1f` y `turnoxop` para identificar llaves primarias, restricciones de unicidad y auditoría.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d bturno1f; \d turnoxop;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
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

**Comentario de Hallazgo**
Se confirma que la unicidad depende de **llaves compuestas** `(compania, turno)`. En Odoo 19, esto requiere concatenar ambos campos para generar `xml_ids` únicos. La tabla `turnoxop` revela una vinculación operativa mediante `nroop` y una gestión por fecha (`fechatur`), lo que facilitará el mapeo hacia órdenes de trabajo. La presencia de campos de auditoría (`usuacreac`, `horultimod`) permitirá validar la integridad de los datos previo a la carga.

---

### SECCIÓN: ANÁLISIS DE DATOS REALES - TABLA MAESTRA `bturno1f`
**Objetivo**
Inspeccionar los datos reales almacenados en la tabla maestra `bturno1f` para comprender los códigos de turno utilizados, la estructura de descripciones y el patrón de replicación por compañía.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM bturno1f LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
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

**Comentario de Hallazgo**
- **Patrón de datos**: Los turnos usan códigos secuenciales de 3 dígitos (`001`, `002`, `003`) representando Primer, Segundo y Tercer turno.
- **Replicación por compañía**: El mismo turno (`001`) existe en múltiples compañías (`0030`, `0032`, `0070`, `0076`, `0081`, `5000`, `0036`), lo que indica que la maestra `bturno1f` es una tabla de definición base sin horarios específicos.
- **Doble descripción**: `descturno1` (ej: `TURNO1`) y `descturno2` (ej: `TURNO 1`) parecen ser variantes de formato para diferentes reportes o interfaces.
- **Fechas julianas**: `feccreacio = 734799` equivale aproximadamente a enero 2010, sugiriendo una carga masiva inicial. El usuario `CPALOMINO` aparece como creador universal.
- **Estado**: Todos los registros muestran `ststurno = A` (Activo) y `estado = A`, sin turnos inactivos visibles.
- **Volumen total**: 30 registros en `bturno1f`.

---

### SECCIÓN: ANÁLISIS DE ESTRUCTURA DDL - TABLAS `relacionturno` Y `turno`
**Objetivo**
Inspeccionar la definición técnica de `relacionturno` (mapeo BM ↔ AVAIL) y `turno` (definición con horarios reales por sucursal).

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d relacionturno; \d turno;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
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
 horultimod | text    |           | not null | 
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

**Comentario de Hallazgo**
- **`relacionturno`**: Tabla de mapeo entre turnos de Big Magic (`turnobm`) y turnos del sistema AVAIL (`turnoav`). Clave primaria compuesta de 4 campos. Creada por `SYSTEM`, sugiere carga automática durante configuración de integración.
- **`turno`**: A diferencia de `bturno1f`, esta tabla contiene `hinicio` y `hfin` en formato `HHMMSS`, definiendo los horarios reales de cada turno. Granularidad por sucursal `(compania, sucursal, turno)`. Banderas `flgidavail` y `flgenuso` (bytea) para integración con AVAIL y control de uso.

---

### SECCIÓN: ANÁLISIS DE DATOS REALES - TABLA `relacionturno` (MAPEO BM ↔ AVAIL)
**Objetivo**
Inspeccionar los datos reales de mapeo entre turnos de Big Magic y AVAIL para entender la correspondencia de códigos entre sistemas.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM relacionturno LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
```text
 compania | sucursal | turnobm | turnoav | estado | feccrea | horcrea | usucrea | fecultmod | horultimod | ultusumod 
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

**Comentario de Hallazgo**
- **Mapeo directo**: La relación es casi 1:1 entre `turnobm` (`001`, `002`, `003`) y `turnoav` (`1`, `2`, `3`), con diferencia de formato (BM usa 3 dígitos, AVAIL usa 1 dígito).
- **Registros duplicados con `turnoav` vacío**: Existen dos registros para el mismo `turnobm = 001` en cada sucursal: uno con `turnoav` vacío y otro con `turnoav = 1`. Esto sugiere un fallback o registro comodín cuando no hay mapeo específico.
- **Creado por SYSTEM**: Todos los registros fueron creados por el usuario `SYSTEM`, indicando carga automática durante configuración de integración con AVAIL.
- **Volumen**: 14 registros totales, cubriendo sucursales `0001`, `0068`, `0070`, `0108` de compañía `0030`.

---

### SECCIÓN: ANÁLISIS DE DATOS REALES - TABLA `turnoxop` (ASIGNACIÓN TURNO ↔ OP)
**Objetivo**
Inspeccionar la tabla transaccional que vincula turnos con órdenes de producción, entendiendo cómo se registra qué turno ejecutó qué OP en qué fecha.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM turnoxop LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
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

**Comentario de Hallazgo**
- **Volumen masivo**: 37,155 registros, confirmando que es la tabla transaccional de mayor actividad relacionada con turnos.
- **Una OP puede tener múltiples turnos**: La OP `PMTY210004` aparece en turnos `001` y `003`, indicando que una orden de producción puede extenderse across múltiples turnos.
- **Prefijos de OP por sucursal**: `PMTY` (Monterrey), `PPUE` (Puebla), `PVHS` (Villa de Salas/Villahermosa), confirmando que el `nroop` incluye código de planta.
- **Usuarios reales**: Los nombres de usuario (`JMACARENO`, `LAPEREZ`, `MGOMEZ`, `RRSALAZAR`, `EDUARDOMG`, etc.) son operadores reales de planta.
- **Índice único**: `(compania, sucursal, fechatur, nroop, turno)` permite que la misma OP se registre en diferentes fechas y turnos, pero no duplicados exactos.

---

### SECCIÓN: ANÁLISIS DE VOLUMENES GLOBALES
**Objetivo**
Obtener el conteo total de registros en todas las tablas de turnos para dimensionar la escala de datos a migrar.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 'bturno1f' as tabla, count(*) FROM bturno1f
UNION ALL SELECT 'relacionturno', count(*) FROM relacionturno
UNION ALL SELECT 'turnoxop', count(*) FROM turnoxop
UNION ALL SELECT 'turno', count(*) FROM turno;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
```text
     tabla     | count 
---------------+-------
 bturno1f      |    30
 relacionturno |    14
 turnoxop      | 37155
 turno         |    55
(4 rows)
```

**Comentario de Hallazgo**
- **Maestras pequeñas**: `bturno1f` (30), `relacionturno` (14), `turno` (55) son tablas de configuración con pocos registros, fáciles de migrar.
- **Transaccional masiva**: `turnoxop` (37,155) contiene el histórico de asignaciones turno-OP. Para Odoo 19, probablemente solo se migren registros del periodo activo, no el histórico completo.
- **Ratio**: ~676 asignaciones turno-OP por turno maestro (37,155 / 55), indicando alta actividad transaccional.

---

### SECCIÓN: ANÁLISIS DE TABLAS TRANSACCIONALES RELACIONADAS - HORAS Y PROGRAMACIÓN DE TURNO
**Objetivo**
Inspeccionar la estructura de tablas que vinculan turnos con horas de trabajo (`horpro`), programación de turno (`proptur`, `dproptur`) y planificación por línea (`opxlinea`), para entender el ecosistema completo de gestión de turnos.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('horpro', 'opxlinea', 'proptur', 'dproptur')
AND table_schema = 'public'
ORDER BY table_name, ordinal_position;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
```text
 table_name | column_name |    data_type     
------------+-------------+------------------
 dproptur   | compania    | text
 dproptur   | sucursal    | text
 dproptur   | fecha       | integer
 dproptur   | turno       | text
 dproptur   | emplead     | integer
 dproptur   | famequip    | text
 dproptur   | linequip    | integer
 dproptur   | secuencia   | double precision
 dproptur   | horaini     | text
 dproptur   | horafin     | text
 dproptur   | observ      | text
 dproptur   | feccrea     | integer
 dproptur   | horcrea     | text
 dproptur   | usucrea     | text
 dproptur   | ultfecmod   | integer
 dproptur   | ulthormod   | text
 dproptur   | ultusumod   | text
 dproptur   | selecc      | bytea
 horpro     | compania    | text
 horpro     | sucursal    | text
 horpro     | nroop       | text
 horpro     | nrosec      | double precision
 horpro     | operacion   | smallint
 horpro     | linea       | integer
 horpro     | fecha       | integer
 horpro     | turno       | text
 horpro     | empleado    | integer
 horpro     | qhoras      | double precision
 horpro     | feccrea     | integer
 horpro     | horcrea     | text
 horpro     | usucrea     | text
 horpro     | ultfecmod   | integer
 horpro     | ulthormod   | text
 horpro     | ultusumod   | text
 horpro     | qhed        | double precision
 horpro     | qhen        | double precision
 horpro     | qhdo        | double precision
 horpro     | qhded       | double precision
 horpro     | qhden       | double precision
 horpro     | qhfo        | double precision
 horpro     | qhfed       | double precision
 horpro     | qhfen       | double precision
 horpro     | vhoras      | double precision
 horpro     | vhed        | double precision
 horpro     | vhen        | double precision
 horpro     | vhdo        | double precision
 horpro     | vhded       | double precision
 horpro     | vhden       | double precision
 horpro     | vhfo        | double precision
 horpro     | vhfed       | double precision
 horpro     | vhfen       | double precision
 horpro     | qhnoc       | double precision
 horpro     | vhnoc       | double precision
 horpro     | vhoras_dol  | double precision
 horpro     | vhed_dol    | double precision
 horpro     | vhen_dol    | double precision
 horpro     | vhdo_dol    | double precision
 horpro     | vhded_dol   | double precision
 horpro     | vhden_dol   | double precision
 horpro     | vhfo_dol    | double precision
 horpro     | vhfed_dol   | double precision
 horpro     | vhfen_dol   | double precision
 horpro     | vhnoc_dol   | double precision
 opxlinea   | compania    | text
 opxlinea   | sucursal    | text
 opxlinea   | fecprg      | integer
 opxlinea   | turno       | text
 opxlinea   | fameqp      | text
 opxlinea   | lineqp      | integer
 opxlinea   | tipenvase   | text
 opxlinea   | formato     | text
 opxlinea   | sabor       | text
 opxlinea   | articulo    | double precision
 opxlinea   | horini      | text
 opxlinea   | horfin      | text
 opxlinea   | cjsprg      | double precision
 opxlinea   | cjseje      | double precision
 opxlinea   | lanzada     | bytea
 opxlinea   | feccrea     | integer
 opxlinea   | horcrea     | text
 opxlinea   | usucrea     | text
 opxlinea   | ultfecmod   | integer
 opxlinea   | ulthormod   | text
 opxlinea   | ultusumod   | text
 opxlinea   | tipdata     | text
 proptur    | compania    | text
 proptur    | sucursal    | text
 proptur    | fecha       | integer
 proptur    | turno       | text
 proptur    | emplead     | integer
 proptur    | tothorprg   | double precision
 proptur    | tothorrep   | double precision
 proptur    | feccrea     | integer
 proptur    | horcrea     | text
 proptur    | usucrea     | text
 proptur    | ultfecmod   | integer
 proptur    | ulthormod   | text
 proptur    | ultusumod   | text
(98 rows)
```

**Comentario de Hallazgo**
- **`horpro` (Horas de Producción)**: Tabla masiva con campos de horas cuantitativas (`qhoras`, `qhed`, `qhen` = horas diurnas, nocturnas, dobles) y valores monetarios (`vhoras`, `vhoras_dol`). Fuente para cálculo de costos de mano de obra por turno.
- **`opxlinea` (Operaciones por Línea)**: Planificación detallada: qué formato, sabor y artículo se produce en qué línea y turno. Incluye `cjsprg` (cajas programadas) y `cjseje` (cajas ejecutadas), base para cálculo de eficiencia.
- **`proptur` (Programación de Turno)**: Resume horas programadas (`tothorprg`) vs reportadas (`tothorrep`) por empleado y turno. Sirve para conciliación de nómina vs producción.
- **`dproptur` (Detalle Programación Turno)**: Nivel más granular con secuencia, hora inicio/fin real y observaciones por empleado y equipo.
- **Implicación para Odoo 19**: Estas tablas no son parte del catálogo de turnos per se, pero son consumidoras críticas del dato "turno". El modelo de turno en Odoo debe ser referenciable desde estas estructuras transaccionales.

---

### SECCIÓN: AUDITORÍA DE TRIGGERS EN TABLAS DE TURNOS
**Objetivo**
Verificar si existen triggers (disparadores) en las tablas de turnos que ejecuten lógica automática de negocio al insertar, actualizar o eliminar registros.

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE event_object_table IN ('bturno1f', 'turnoxop', 'relacionturno', 'turno');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
```text
 trigger_name | event_manipulation | event_object_table 
--------------+--------------------+--------------------
(0 rows)
```

**Comentario de Hallazgo**
- **Sin triggers**: No existen disparadores en ninguna de las 4 tablas de turnos. Toda la lógica de negocio (validaciones, cascadas, auditoría) está implementada en la capa de aplicación (código del ERP legacy), no en la base de datos.
- **Ventaja para migración**: Al no haber lógica embebida en triggers, la migración a Odoo 19 es más limpia: toda la lógica se reimplementará en los modelos Python de Odoo (`models/`), con mayor control y trazabilidad.
- **Riesgo mitigado**: No hay efectos colaterales ocultos que deban replicarse; el comportamiento del sistema es completamente determinista desde la capa de aplicación.

---

### SECCIÓN: ANÁLISIS DE DATOS REALES - TABLA `turno` (HORARIOS POR SUCURSAL)
**Objetivo**
Inspeccionar los datos reales de horarios de turnos para comprender las variaciones entre sucursales y los patrones de turnos cruzados (nocturnos que cruzan medianoche).

**Comando (Bash)**
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT * FROM turno LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```

**Resultado**
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

**Comentario de Hallazgo**
- **Variación de horarios por sucursal**: 
  - Sucursal `0032/0001`: Turno 1 de `06:30` a `14:30`, Turno 2 de `14:30` a `22:00`, Turno 3 de `22:00` a `06:30`
  - Sucursal `0035/09`: Turno 1 de `07:00` a `15:00`, Turno 2 de `15:00` a `23:00`, Turno 3 de `23:00` a `07:00`
  - Cada planta/sucursal define sus propios horarios operativos.
- **Turnos cruzados**: El Tercer Turno siempre cruza medianoche (ej: `220000` → `063000`), lo que implica lógica especial para asignar producción al turno correcto cuando una OP inicia un día y termina al siguiente.
- **Continuidad sin traslape**: Los horarios son contiguos (fin de uno = inicio del siguiente), sin gaps ni solapamientos.
- **Banderas AVAIL**: `\x46` en `flgidavail` y `flgenuso` representa el byte ASCII `F` (False), indicando que estos turnos no están marcados para integración directa con AVAIL o están en modo de solo uso local.


### Seccion: Auditoria de programacion operativa - Tabla OPXLINEA
Se busca analizar la relacion entre la programacion de produccion, las lineas de equipo y los turnos para validar la integridad de los datos de manufactura en **opxlinea**

```bash
esau@DESKTOP-A3RPEKP:~/TutorialOdoo$ docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='PASSWORD' && echo \"SELECT compania, sucursal, fecprg, turno, fameqp, lineqp, tipenvase, formato, sabor, cjsprg, cjseje FROM opxlinea LIMIT 15;\" | psql -h IP -U postgres -d mxbdaje_local"
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


**comentario**
1. AGENTE COMPLETA TU ANALISIS

### Seccion. Auditoria de tiempos improductivos - Tabla PARPROD
Se busca inspeccionar la estructura y los datos de la tabla **parprod** para entender cómo se registran los paros de linea y su vinculacion con los turnos operativos.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='PASSWORD' && echo '\d parprod; SELECT compania, sucursal, fecha, nroturno, ultturno FROM parprod LIMIT 10;' | psql -h IP -U postgres -d mxbdaje_local"
```

```text
 Table "public.parprod"
     Column     |       Type       | Collation | Nullable | Default 
----------------+------------------+-----------+----------+---------
 compania       | text             |           |          | 
 codigo         | smallint         |           |          | 
 inc            | text             |           |          | 
 ind            | text             |           |          | 
 despachoma     | text             |           |          | 
 devdisp        | text             |           |          | 
 devrechaza     | text             |           |          | 
 dvc            | text             |           |          | 
 trancontro     | text             |           |          | 
 parteing       | text             |           |          | 
 tranajting     | text             |           |          | 
 tranajtsal     | text             |           |          | 
 salmstr        | text             |           |          | 
 mpi            | text             |           |          | 
 mps            | text             |           |          | 
 cliente        | integer          |           |          | 
 reqprod        | text             |           |          | 
 tranoprod      | text             |           |          | 
 tranocomp      | text             |           |          | 
 tranreq        | text             |           |          | 
 trantra        | text             |           |          | 
 actrcal        | text             |           |          | 
 aprduc         | text             |           |          | 
 feccrea        | integer          |           |          | 
 horcrea        | text             |           |          | 
 usucrea        | text             |           |          | 
 fecultimod     | integer          |           |          | 
 horultimod     | text             |           |          | 
 usuultimod     | text             |           |          | 
 nroturno       | smallint         |           |          | 
 horaxtur       | smallint         |           |          | 
 diaxmes        | smallint         |           |          | 
 reqalmlog      | text             |           |          | 
 famenv         | text             |           |          | 
 famsop         | text             |           |          | 
 famjar         | text             |           |          | 
 aprobot        | text             |           |          | 
 proreqpro      | smallint         |           |          | 
 cotizacion     | text             |           |          | 
 tipartser      | text             |           |          | 
 almcont        | text             |           |          | 
 devmer         | text             |           |          | 
 protocolos     | text             |           |          | 
 salidacc       | text             |           |          | 
 falpro         | text             |           |          | 
 sobpro         | text             |           |          | 
 trnconmue      | text             |           |          | 
 manejo_x_racks | bytea            |           |          | 
 faccjs         | double precision |           |          | 
 plapro         | text             |           |          | 
 savvar         | text             |           |          | 
 faminy         | text             |           |          | 
 famazu         | text             |           |          | 
 libre1         | text             |           |          | 
 libre2         | text             |           |          | 
 libre3         | text             |           |          | 
 libre4         | text             |           |          | 
 libre5         | text             |           |          | 
 libre6         | text             |           |          | 
 libre7         | text             |           |          | 
 libre8         | double precision |           |          | 
 libre9         | double precision |           |          | 
 libre10        | double precision |           |          | 
 libre11        | double precision |           |          | 
 areman         | text             |           |          | 
 aretag         | text             |           |          | 
 areazu         | text             |           |          | 
 arejara        | text             |           |          | 
 arelvbt        | text             |           |          | 
 arelifz        | text             |           |          | 
 arebb          | text             |           |          | 
 almvalr        | text             |           |          | 
 almvalg        | text             |           |          | 
 almnovg        | text             |           |          | 
 almnovr        | text             |           |          | 
 libre12        | text             |           |          | 
 libre13        | text             |           |          | 
 libre14        | text             |           |          | 
 libre15        | text             |           |          | 
 areemb         | text             |           |          | 
 areiso         | text             |           |          | 
 famemb         | text             |           |          | 
 famiso         | text             |           |          | 
 linmpmp        | text             |           |          | 
 linmpis        | text             |           |          | 
 linrefrp       | text             |           |          | 
 linrefpg       | text             |           |          | 
 lingesm        | text             |           |          | 
 lingesmp       | text             |           |          | 
 ctptvta        | text             |           |          | 
 ctptded        | text             |           |          | 
 ctptcob        | text             |           |          | 
 ctptdif        | text             |           |          | 
 tartprt        | text             |           |          | 
 famjbag        | text             |           |          | 
 famjbiso       | text             |           |          | 
 arenect        | text             |           |          | 
 famjnec        | text             |           |          | 
 famnect        | text             |           |          | 
 areminy        | text             |           |          | 
 famminy        | text             |           |          | 
 trasptin       | text             |           |          | 
 vtamaqui       | text             |           |          | 
 cdogtoind      | text             |           |          | 
 sucprin        | text             |           |          | 
 tramuest       | text             |           |          | 
 trarqalm       | text             |           |          | 
 almproc        | text             |           |          | 
 trasalaut      | text             |           |          | 
 traingaut      | text             |           |          | 
 famresina      | text             |           |          | 
 ultturno       | text             |           |          | 
 diastkseg      | smallint         |           |          | 
 actalmpro      | bytea            |           |          | 
 tranvalno      | text             |           |          | 
 tipartins      | text             |           |          | 
 tipartemp      | text             |           |          | 
 trandocref     | text             |           |          | 
 tradevprov     | text             |           |          | 
 almmp          | text             |           |          | 
 almcon         | text             |           |          | 
 almconref      | text             |           |          | 
 almcongen      | text             |           |          | 
 trasalcon      | text             |           |          | 
 traingcon      | text             |           |          | 
 almafijo       | text             |           |          | 
 flgatepro      | bytea            |           |          | 
Indexes:
    "idx_172135_parprod1" UNIQUE, btree (compania, codigo)

\d: extra argument "SELECT" ignored
\d: extra argument "compania," ignored
\d: extra argument "sucursal," ignored
\d: extra argument "fecha," ignored
\d: extra argument "nroturno," ignored
\d: extra argument "ultturno" ignored
\d: extra argument "FROM" ignored
\d: extra argument "parprod" ignored
\d: extra argument "LIMIT" ignored
\d: extra argument "10;" ignored
```
**comentarios**


### seccion : Auditoria de parametros de produccion - Tabla PARPROD (complemento de la seccion anterior)
**objetivo** : inspeccionar la estructura tecnica y el contenido de la tabla **parprod** para identificar parametros operativos globales

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='PASS' && echo \"SELECT compania, codigo, nroturno, ultturno, feccrea FROM parprod LIMIT 10;\" | psql -h IP -U postgres -d mxbdaje_local"
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

**comentario**

### Seccion : Alcance Operativo - Segmentacion de Turnos por Sucursal 
**objetivo**: identificar el alcance real de las sucursales que tienen turnos configurados, con el fi de determinar la complejidad del despliegue multi-compañia en Odoo 19.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='PASS' && echo \"SELECT DISTINCT compania, sucursal FROM turno ORDER BY compania, sucursal;\" | psql -h IP -U postgres -d mxbdaje_local"
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

**comentario**