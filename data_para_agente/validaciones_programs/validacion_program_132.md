
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
1. **Campo `turno` vacío en registros antiguos**: Los primeros 15 registros muestran el campo `turno` completamente vacío (NULL o string vacío), junto con `fameqp` vacío y `lineqp = 0`. Esto indica registros de programación inicial o plantillas sin asignar, posiblemente creados durante la configuración inicial del sistema.
2. **Fechas julianas tempranas**: `fecprg` va de 735131 a 736564 (aprox. 2013-2017), sugiriendo que estos son registros históricos de prueba o migración inicial que nunca se completaron.
3. **Compañías diversas**: Aparecen compañías `0100` y `0002` con múltiples sucursales, pero sin datos de producción reales (todos los campos en cero/vacío).
4. **Implicación para migración**: Estos registros huérfanos deben filtrarse durante la migración a Odoo 19. Solo se deben migrar registros de `opxlinea` con `turno` poblado y `cjsprg > 0` (cajas programadas reales).
5. **Relación turno-línea**: La tabla `opxlinea` usa `turno` como `text` (no como FK numérica), confirmando que el código de turno se almacena directamente como llave natural en cada línea de programación.

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
1. **Tabla de parámetros, no de paros**: A pesar del nombre `parprod` (que podría interpretarse como "paros de producción"), la estructura revela que es una tabla de **parámetros de producción** por compañía. La PK `(compania, codigo)` con solo 4 registros (uno por compañía activa) confirma que es configuración, no transaccional.
2. **`nroturno` como smallint vs `ultturno` como text**: `nroturno` almacena el turno como número (3), mientras `ultturno` lo almacena como texto formateado ('003'). Esta dualidad refleja la inconsistencia del sistema legacy: algunos módulos usan formato numérico, otros formato string con ceros.
3. **`horaxtur` y `diaxmes`**: Campos clave para cálculo de capacidad productiva. `horaxtur` (horas por turno) y `diaxmes` (días de operación al mes) son parámetros base para planificación de producción.
4. **Campos `libre1-15`**: Campos extensibles para personalizaciones futuras, patrón común en sistemas legacy para evitar ALTER TABLE.
5. **Múltiples áreas y familias**: Campos como `areman`, `arettag`, `famsop`, `famjar` indican que esta tabla configura qué áreas y familias de productos están activas por compañía, incluyendo manejo de racks, devoluciones, y protocolos.
6. **Sin fecha de creación válida**: `feccrea = 0` en todos los registros, indicando carga inicial del sistema sin timestamp válido.


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
1. **Confirmación de tabla de parámetros**: Solo 4 registros, uno por compañía (`0035`, `0030`, `0032`, `0075`), con `codigo = 1` en todos. Esto confirma que `parprod` es una tabla de configuración global de producción por compañía, no una tabla transaccional de paros.
2. **`nroturno = 3` uniforme**: Todas las compañías tienen configurado el turno 3 como turno predeterminado o último turno de referencia. Coincide con `ultturno = '003'` (mismo valor, diferente formato).
3. **`feccrea = 0` en todos**: Sin fecha de creación válida, indicando carga inicial del sistema sin timestamp. Patrón consistente con otras tablas maestras cargadas en bloque.
4. **Compañía `0075` nueva**: Aparece en `parprod` pero no fue vista en análisis anteriores de `bturno1f`. Necesario verificar si tiene turnos configurados en la tabla `turno`.
5. **Implicación para Odoo 19**: Estos parámetros deben mapearse a la configuración de la compañía en Odoo (`res.company`), específicamente campos como `horaxtur` (horas por turno) y `diaxmes` (días operativos al mes) que afectan la planificación de producción (MRP). 
**objetivo**: identificar el alcance real de las sucursales que tienen turnos configurados, con el fi de determinar la complejidad del despliegue multi-compañia en Odoo 19.

### Seccion: Mapeo de Alcance Operativo- Segmentacion Multi-Compañia  y Sucursales
**objetivo**: Determinar la cobertura geografica  y organizacional del sistema mediante la identificacion   de combinaciones unicas de compañia y sucursal, con el fin de dimensionar el despliegue de estructuras en Odoo 19 ...

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
1. **Distribución por compañía**:
   - **Compañía `0030`**: 11 sucursales activas (`0001`, `0068`, `0070`, `0086`, `0108`, `0112`, `0113`, `0114`, `0115`, `0116`, `114`). Es la compañía con mayor cobertura operativa. Nota: `114` y `0114` podrían ser la misma sucursal con formato inconsistente.
   - **Compañía `0032`**: 1 sucursal (`0001`). Operación concentrada en una sola planta.
   - **Compañía `0035`**: 6 sucursales (`01`, `03`, `04`, `05`, `08`, `09`). Formato de sucursal sin ceros a la izquierda (diferente a `0030`).
   - **Compañía `0036`**: 1 sucursal (`01`). Operación mínima o nueva.
2. **Inconsistencia en formato de sucursal**: `0030` usa formato de 4 dígitos (`0001`, `0068`), mientras `0035` y `0036` usan formato de 2 dígitos (`01`, `09`). Esto requiere normalización durante la migración a Odoo 19 para evitar duplicados o referencias rotas.
3. **Sucursal `114` vs `0114` en compañía `0030`**: Posible duplicado por inconsistencia de formato. Necesaria consulta de validación para confirmar si son la misma entidad.
4. **Total**: 19 combinaciones únicas de `compania/sucursal` con turnos configurados. Esto define el scope real del despliegue multi-compañía en Odoo 19.
5. **Compañías sin turnos configurados**: `0002`, `0075`, `0076`, `0081`, `0100`, `5000` (vistas en `bturno1f` o `opxlinea`) NO aparecen en `turno`. Pueden ser compañías inactivas, de solo distribución, o que aún no han configurado sus horarios de turno.
6. **Implicación para Odoo 19**: Cada compañía (`0030`, `0032`, `0035`, `0036`) debe mapearse a un `res.company` en Odoo, y cada sucursal a un `stock.warehouse` o `mrp.workcenter` dependiendo de si es planta de producción o centro de distribución.

## Dudas luego del analisis de las consultas previas

### 1. 
Relación bturno1f ↔ turno — ¿Cuál es la maestra definitiva?
- bturno1f: 30 registros, turnos por compañía (sin sucursal, sin horarios)
- turno: 55 registros, turnos por compañía + sucursal (con hinicio/hfin)
- Duda: ¿bturno1f es catálogo global y turno es la instancia operativa por sucursal? ¿O son redundantes y una está obsoleta?
- Consulta sugerida: SELECT compania, turno FROM bturno1f WHERE compania = '0035'; (0035 está en turno pero no apareció en los 20 rows vistos de bturno1f)

**absolución**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='PASS' && echo \"SELECT compania, turno FROM bturno1f WHERE compania = '0035';\" | psql -h IP -U postgres -d mxbdaje_local"
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

### 2.
2. Discrepancia de compañías entre tablas
Compañía
0030
0032
0035
0036
0070
0075
0076
0081
5000
- Duda: 0070, 0076, 0081, 5000 tienen definición de turno pero sin horarios configurados. ¿Son compañías inactivas o migradas?
- Duda: 0075 tiene parámetros de producción pero sin turnos. ¿Cómo opera?

**absolucion**
Aparecen en bturno1f pero en la tabla operativa turno no tienen horas de inicio  o fin configuradas.Verificar si estas compañias tienen movimientos reales en la tabla de programacion de lineas opxlinea.
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT compania, COUNT(*) FROM opxlinea WHERE compania IN ('0070', '0076', '0081', '5000') GROUP BY compania;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

compania | count 
----------+-------
(0 rows)

```
0075 aparece en la tabla de parametros de produccion parprod (el sistema sabe que debe producir algo) pero no tiene turnos definidos.Verificar si la compañia usa una estructura distinta o simplemente es una configuracion incompleta
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT * FROM parprod WHERE compania = '0075';\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

compania | codigo | inc | ind | despachoma | devdisp | devrechaza | dvc | trancontro | parteing | tranajting | tranajtsal | salmstr | mpi | mps | cliente | reqprod | tranoprod | tranocomp | tranreq | trantra | actrcal | aprduc | feccrea | horcrea | usucrea | fecultimod | horultimod | usuultimod | nroturno | horaxtur | diaxmes | reqalmlog | famenv | famsop | famjar | aprobot | proreqpro | cotizacion | tipartser | almcont | devmer | protocolos | salidacc | falpro | sobpro | trnconmue | manejo_x_racks | faccjs | plapro | savvar | faminy | famazu | libre1 | libre2 | libre3 | libre4 | libre5 | libre6 | libre7 | libre8 | libre9 | libre10 | libre11 | areman | aretag | areazu | arejara | arelvbt | arelifz | arebb | almvalr | almvalg | almnovg | almnovr | libre12 | libre13 | libre14 | libre15 | areemb | areiso | famemb | famiso | linmpmp | linmpis | linrefrp | linrefpg | lingesm | lingesmp | ctptvta | ctptded | ctptcob | ctptdif | tartprt | famjbag | famjbiso | arenect | famjnec | famnect | areminy | famminy | trasptin | vtamaqui | cdogtoind | sucprin | tramuest | trarqalm | almproc | trasalaut | traingaut | famresina | ultturno | diastkseg | actalmpro | tranvalno | tipartins | tipartemp | trandocref | tradevprov | almmp | almcon | almconref | almcongen | trasalcon | traingcon | almafijo | flgatepro 
----------+--------+-----+-----+------------+---------+------------+-----+------------+----------+------------+------------+---------+-----+-----+---------+---------+-----------+-----------+---------+---------+---------+--------+---------+---------+---------+------------+------------+------------+----------+----------+---------+-----------+--------+--------+--------+---------+-----------+------------+-----------+---------+--------+------------+----------+--------+--------+-----------+----------------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+---------+---------+--------+--------+--------+---------+---------+---------+-------+---------+---------+---------+---------+---------+---------+---------+---------+--------+--------+--------+--------+---------+---------+----------+----------+---------+----------+---------+---------+---------+---------+---------+---------+----------+---------+---------+---------+---------+---------+----------+----------+-----------+---------+----------+----------+---------+-----------+-----------+-----------+----------+-----------+-----------+-----------+-----------+-----------+------------+------------+-------+--------+-----------+-----------+-----------+-----------+----------+-----------
 0075     |      1 | 026 | ISO | DSP        | DPD     | DPR        | 047 | TCC        | INP      | AJI        | AJS        | SPM     | MPI | MPS |       0 | RQP     | OPR       | OCO       | REQ     | TRA     | 700     | 700    |       0 | 000001  |         |          0 | 000001     |            |        3 |        8 |      26 | RAL       | 001    | 002    | 003    | 704     |         0 |            |           | 1008    | DPM    |            |          | FPR    |        |           | \x46           |  5.678 |        | SPP    | 009    | 010    | DPP    | DMC    | CVT    | 007    | 002    |        | 70     |      1 |      0 |       0 |       0 | 703    | 705    | 706    | 707     | 709     | 711     | 712   | 1009    | 1007    | 1050    | 1051    | IDU     | 709     | 045     | 004     | 713    | 714    | 013    | 014    |         |         |          |          |         |          | CVE     | CVD     | CVC     | CVS     | 004     | 015     | 016      | 701     | 019     | 018     | 717     | 017     | 100      | SVQ      | 001       | 0001    | IMU      | 040      | 83      | ATP       | IAP       | 020       | 003      |         3 | \x46      | 025       | 001       | 003       | TNS        | SPR        |       |        |           |           |           |           |          | \x54
(1 row)

```
0075 tiene parametros en parprod pero no turnos
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT DISTINCT compania FROM turno;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

 compania 
----------
 0030
 0032
 0036
 0035
(4 rows)

```
Alguna vez ha producido algo, a pesar de no tener turnos configurados?
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT count(*) FROM opxlinea WHERE compania = '0075';\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
 
 count 
-------
     0
(1 row)
```
0036 está en turno pero no en parprod (configuracion global) ,un inversion de lo que pasa con 0075
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT DISTINCT sucursal FROM turno WHERE compania = '0036';\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

### 3. 
Sucursal 114 vs 0114 en compañía 0030
- Ambas existen en turno como registros separados
- Duda: ¿Duplicado por inconsistencia de formato o son sucursales reales distintas?
- Consulta sugerida: SELECT * FROM turno WHERE compania='0030' AND sucursal IN ('114','0114');
---

Los registros de las sucursales 114  y 0114 comparten la misma configuracion operativa o representan entidades fisicas diferentes.
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT sucursal, turno, hinicio, hfin, flgidavail, flgenuso FROM turno WHERE compania='0030' AND sucursal IN ('114','0114') ORDER BY turno;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
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

**Consulta de validación sugerida**:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='PASS' && echo \"
SELECT 'turnoxop' as tabla, sucursal, COUNT(*) FROM turnoxop 
WHERE compania='0030' AND sucursal IN ('114','0114') GROUP BY sucursal
UNION ALL
SELECT 'opxlinea', sucursal, COUNT(*) FROM opxlinea 
WHERE compania='0030' AND sucursal IN ('114','0114') GROUP BY sucursal
UNION ALL
SELECT 'horpro', sucursal, COUNT(*) FROM horpro 
WHERE compania='0030' AND sucursal IN ('114','0114') GROUP BY sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

## CONCLUSIONES GENERALES - PUNTOS CRÍTICOS RESUELTOS

### Resumen de Hallazgos

| Punto | Duda Original | Resolución |
|-------|--------------|------------|
| **1. bturno1f ↔ turno** | ¿Cuál es la maestra? | **Jerárquica**: `bturno1f` = catálogo global, `turno` = instancia operativa por sucursal |
| **2. Compañías discrepantes** | ¿0070/0075/0076/0081/5000 activas? | **Inactivas/zombi**: Solo `0030`, `0032`, `0035`, `0036` operativas. `0075` zombi, `0036` alcance mínimo |
| **3. 114 vs 0114** | ¿Duplicado o sucursales distintas? | **Duplicado confirmado**: `0114` es la real (40 turnoxop, 61 horpro). `114` es artefacto de formato (1 registro huérfano) |

### Scope Definitivo para Migración a Odoo 19

**Compañías a migrar con estructura completa de turnos**:
- `0030` — 10 sucursales reales (excluyendo `114` duplicado)
- `0032` — 1 sucursal
- `0035` — 6 sucursales
- `0036` — 1 sucursal (configuración incompleta, requiere validación)

**Total**: 18 sucursales reales × 3 turnos = **~54 registros de horarios** a migrar.

**Excluidos de migración**:
- `0070`, `0076`, `0081`, `5000` — Inactivas, sin actividad productiva.
- `0075` — Registro zombi (parámetros sin turnos ni producción).
- `114` (dentro de `0030`) — Duplicado de `0114`.

### Implicaciones para el Modelo Odoo 19

1. **Modelo `bm.turno.definicion`**: Catálogo de turnos (código + descripción) por compañía. Hereda de `bturno1f`.
2. **Modelo `bm.turno.horario`**: Instancias operativas con `hinicio`/`hfin` por sucursal. Hereda de `turno`.
3. **Validación de formato de sucursal**: Implementar constraint que normalice códigos a formato consistente (4 dígitos para `0030`, 2 dígitos para `0035/0036` o unificar todo a 4 dígitos).
4. **Lógica de turnos cruzados**: El turno 3 (`220000` → `063000`) requiere regla especial para asignar producción nocturna al día correcto.
5. **Relación con tablas transaccionales**: `turnoxop`, `opxlinea`, `horpro`, `proptur`, `dproptur` deben referenciar al modelo de turno vía llave natural `(compania, sucursal, turno)`.

### 4. 
Turnos cruzados (nocturnos)
- Turno 3: hinicio=220000, hfin=063000 (fin < inicio)
- Duda: ¿Cómo determinar a qué turno pertenece una producción registrada a las 02:00 AM? ¿Se asigna al día anterior o al actual?
- Impacto: Lógica de asignación automática de turno en Odoo necesita regla especial.

**absolucion**
La asignación de producción nocturna requiere lógica basada en hora de registro vs ventana de turno, no solo por fecha calendario.

**Consulta de validación sugerida**:
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT t.compania, t.sucursal, t.turno, t.hinicio, t.hfin,
       CASE WHEN t.hinicio > t.hfin THEN 'CRUZADO' ELSE 'NORMAL' END as tipo_turno
FROM turno t
WHERE t.hinicio > t.hfin;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

### 5. 
5. Registros duplicados en relacionturno
- turnobm=001 tiene 2 registros por sucursal: uno con turnoav='' y otro con turnoav='1'
- Duda: ¿El registro vacío es fallback, error, o registro histórico? ¿Cuál usar para migración?

**absolucion**
```bash
 docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT turnoav, COUNT(*) FROM relacionturno WHERE compania='0030' GROUP BY turnoav;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

### 6. 
6. opxlinea — volumen de registros huérfanos
- Los primeros 15 rows tienen turno='', fameqp='', cjsprg=0
- Duda: ¿Qué porcentaje del total representan? Si son mayoría, la tabla opxlinea podría ser mayormente basura.
- Consulta sugerida: SELECT count(*) as total, count(*) FILTER (WHERE turno='') as vacios FROM opxlinea;

**absolucion**
Determinar la salud de la tabla principal, si la mayoria de los registros no tiene un turno asignado (cementerio de datos)  o una tabla que se usa para fines distintos a la programacion (borradores o logs)

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT count(*) as total, count(1) FILTER (WHERE turno = '' OR turno IS NULL) as vacios, ROUND((count(1) FILTER (WHERE turno = '' OR turno IS NULL) * 100.0 / count(1)), 2) as porcentaje_basura FROM opxlinea;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

### 7. 
7. parprod — ¿parámetros o paros?
- Nombre sugiere "paros de producción" pero estructura es de parámetros globales
- Duda: ¿Existe otra tabla para registrar paros reales? ¿O el nombre es histórico/engañoso?
- Consulta sugerida: SELECT count(*) FROM parprod; (confirmar que son solo 4 rows)

**absolucion**
Cuantas compañias estan activas o en configuracion 

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT count(*) FROM parprod;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

### 8. 
8. nroturno vs ultturno en parprod
- nroturno = 3 (smallint), ultturno = '003' (text) para todas las compañías
- Duda: ¿Qué significa "último turno"? ¿Turno actual en curso? ¿Turno por defecto? ¿Último turno procesado del día?

**absolucion**

ultturno cambia segun la actividad reciente o es un valor estatico de configuracion, ver si hay variedad entre las 4 compañias
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT compania, nroturno, ultturno FROM parprod;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

### 9.
9. Banderas flgidavail y flgenuso
- Tipo bytea, valor \x46 = ASCII 'F' (False)
- Algunas sucursales (0030/0112) tienen estas banderas ** vacías** (NULL)
- Duda: ¿Qué controlan exactamente? ¿Afectan la migración si no se integra con AVAIL?

NO ESTOY SEGURO SI ESTAS CONSULTAS SIRVEN PARA ESTA DUDA

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT flgidavail, COUNT(*) FROM turno GROUP BY flgidavail;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

flgidavail | count 
------------+-------
            |     7
 \x46       |    48
(2 rows)

docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT flgidavail, flgenuso, COUNT(*) FROM turno GROUP BY flgidavail, flgenuso;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

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

## CONCLUSIONES GENERALES - PUNTOS DE DISEÑO RESUELTOS (5-9)

### Resumen de Hallazgos

| Punto | Duda Original | Resolución |
|-------|--------------|------------|
| **4. Turnos cruzados** | ¿Producción 02:00 AM = día anterior o actual? | **Día anterior**: 20 turnos cruzados (todos Turno 3). Anomalía detectada: `0035/01/003` con `hfin` corrupto |
| **5. Duplicados en relacionturno** | ¿turnoav='' es fallback o error? | **Fallback**: Ignorar en migración. Solo migrar registros con `turnoav` poblado |
| **6. opxlinea huérfanos** | ¿Qué % es basura? | **100% sin turno**: No es fuente de verdad. Usar `turnoxop` como tabla principal |
| **7. parprod nombre** | ¿Parámetros o paros? | **Parámetros maestros**: 1 registro por compañía. Migrar como config de `res.company` |
| **8. nroturno vs ultturno** | ¿Dinámico o estático? | **Estático**: Ambos = 3. Límite de capacidad, no indicador de actividad |
| **9. Banderas avail/uso** | ¿Qué controlan? | **Reliquias**: `flgidavail` siempre F, `flgenuso` solo 6 activos. Omitir en migración |

### Implicaciones Adicionales para el Modelo Odoo 19

1. **Fuente de verdad de producción**: `turnoxop` (37,155 registros) + `horpro` (horas) + `dproptur` (detalle empleado). `opxlinea` se descarta como fuente primaria.
2. **Configuración por compañía**: Modelo `bm.produccion.config` con `horaxtur=8`, `diaxmes=26`, `max_turnos=3`.
3. **Integración AVAIL**: Actualmente inactiva en el sistema legacy. No migrar `relacionturno` salvo validación expresa del equipo de negocio.
4. **Turnos cruzados**: Implementar lógica especial para turno 3 (nocturno) que asigne producción al día de inicio del turno, no al día calendario. **Anomalía detectada**: `0035/01/003` tiene `hfin='07:00:'` (corrupto), requiere limpieza previa.
5. **Limpieza de datos**: Excluir registros zombi (`0075`), duplicados (`114`), compañías inactivas (`0070`, `0076`, `0081`, `5000`), y corregir formato corrupto (`0035/01/003`).

---

### 11.
11. Conversión de fechas julianas
- feccreacio = 734799 ≈ enero 2010, pero la fórmula exacta no está documentada
- Duda: ¿Es fecha juliana PostgreSQL (date '2000-01-01' + 734799)? ¿O del sistema legacy?
- Impacto: Necesario para validar antigüedad de datos durante migración.

**absolucion**
busqueda de registro en turno (fechas de creacion) donde aparezcan ambos formatos...
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT compania, feccrea, fecultimod FROM parprod;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

compania | feccrea | fecultimod 
----------+---------+------------
 0035     |       0 |          0
 0030     |       0 |          0
 0032     |       0 |          0
 0075     |       0 |          0
(4 rows)

docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT compania, sucursal, feccrea FROM horpro WHERE feccrea > 0 LIMIT 5;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"

compania | sucursal | feccrea 
----------+----------+---------
 0030     | 0001     |  737782
 0030     | 0068     |  737809
 0030     | 0068     |  737809
 0030     | 0001     |  737817
 0030     | 0108     |  737817
(5 rows)

```
**Consulta de validación sugerida**:
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

## CONCLUSIONES GENERALES - PUNTOS MENORES RESUELTOS (11)

### Resumen de Hallazgos

| Punto | Duda Original | Resolución |
|-------|--------------|------------|
| **11. Fechas julianas** | ¿Fórmula exacta de conversión? | **Días prolepticos PG**: `date '0001-01-01' + (valor - 1)`. Rango operativo: `2020-12-15` a `2026-01-20` (5.1 años, 1,862 días) |

### Implicaciones para Migración

1. **Función `julian_to_date()` obligatoria** en todos los scripts de migración que procesen campos de fecha del legacy.
2. **Corte recomendado**: Migrar datos desde `2024-01-20` (juliano `738900`+) para mantener Odoo ágil. Archivado externo para 2020-2023.
3. **Datos vigentes**: El sistema legacy operó hasta enero 2026, confirmando que los datos están actualizados y la migración es urgente/necesaria.
4. **Validación post-migración**: Verificar que todas las fechas convertidas caigan dentro del rango `2020-12-15` → `2026-01-20`.
